import re
import json

import graphql
from graphql.language.visitor import Visitor, visit
from typing import Any, List


class LazyVisitor(Visitor):

    def __init__(self):
        self.branch = {}
        self.trail = []

    def _accumulate(self, key, value):
        if isinstance(self.branch, list):
            if key is not None:
                self.branch.append({key: value})
                return
            self.branch.append(value)
        elif isinstance(self.branch, dict):
            self.branch[key] = value

    def enter_selection_set(self, node, key, parent, *_args: Any) -> str:
        if type(parent).__name__ == "OperationDefinitionNode":
            self.trail.append(self.branch)
            self.branch = []

    def leave_selection_set(self, node, key, parent, *_args: Any) -> str:
        if type(parent).__name__ == "OperationDefinitionNode":
            saved, self.branch = self.branch, self.trail.pop(-1)
            self._accumulate(_title(parent), saved)

    def enter_field(self, node, *_args: Any) -> str:
        if node.name.value == "error":
            return
        self.trail.append(self.branch)
        self.branch = {}

    def leave_field(self, node, *_args: Any) -> str:
        if node.name.value == "error":
            return
        saved, self.branch = self.branch, self.trail.pop(-1)
        self._accumulate(node.name.value, saved)

    def enter_object_value(self, *_args: Any) -> str:
        self.trail.append(self.branch)
        self.branch = {}

    def leave_object_value(self, node, key, parent, *_args: Any) -> str:
        saved, self.branch = self.branch, self.trail.pop(-1)
        self._accumulate(_title(parent), saved)

    def enter_list_value(self, *_args: Any) -> str:
        self.trail.append(self.branch)
        self.branch = []

    def leave_list_value(self, node, key, parent, *_args: Any) -> str:
        saved, self.branch = self.branch, self.trail.pop(-1)
        self._accumulate(parent.name.value, saved)

    def leave_string_value(self, node, key: str, path, *_args: Any) -> str:
        self._accumulate(_title(path), node.value)

    def leave_boolean_value(self, node, key: str, path, *_args: Any) -> str:
        self._accumulate(_title(path), bool(node.value))

    def leave_null_value(self, node, key: str, path, *_args: Any) -> str:
        self._accumulate(_title(path), None)

    def leave_int_value(self, node, key: str, path, *_args: Any) -> str:
        self._accumulate(_title(path), int(node.value))

    def leave_float_value(self, node, key: str, path, *_args: Any) -> str:
        self._accumulate(_title(path), float(node.value))

def _title(path):
    return getattr(getattr(path, "name", None), "value", None)

_action_parser = re.compile("^(add|put|delete|update|create)_?(.*)$")

def parse_mutations(inputs: List[str]):
    mutation = " ".join(["mutation m {"] + inputs + ["}"])
    ast = graphql.parse(graphql.Source(mutation, "GraphQL request"))
    visitor = LazyVisitor()
    visit(ast, visitor)
    new_output = []
    for item in visitor.branch["m"]:
        for operation, arguments in item.items():
            op, user_type = _action_parser.match(operation).groups()
            new_output.append({"operation": op, "__typename": user_type, "arguments": arguments})
    return new_output

if __name__ == "__main__":
    sample = [
        """
    addAnimal(
        id:"9cc720d4-623c-11eb-9c41-5391fa973328",
        input: {
            organization_id: "6fe94056-5bd4-11eb-a9fc-0bb70a7f9c77" ,
            name: "bangu" ,
            type: "dog" ,
            sex: "female" ,
            animal_description: "" ,
            primary_color: "Black" ,
            primary_color_group: "black" ,
            additional_colors: [{name: "Blue" , group: "blue" }] ,
            additional_color_groups_string: ["blue"]
        }
    ) {
        error
    }""",
        """
    addEvent(
        id: "b4de7525-623b-11eb-a0cb-0db0d645b658"
        input: {
            animal_id: "b434d448-623b-11eb-afea-59074c0526d3",
            organization_id: "6fe94056-5bd4-11eb-a9fc-0bb70a7f9c77",
            timestamp: 1611929411261,
            node_created: "Node-2",
            type: "intake",
            nested: {thing: ["intake"]},
            sub_type: "Stray/OTC",
            location_description: "",
            three_legged: false,
            tentacles: null,
            address1: "",
            address2: "",
            city: "", state: "", zipcode: "", geo_location: [0.0, 1.0]}
    ) {
        error
    }""",
    ]
    out = parse_mutations(sample)
    print(json.dumps(out, indent=2, sort_keys=True))
