import re
import json

from actions import Action
import graphql
from graphql.language import visitor, Visitor
from graphql.language.ast import ArgumentNode, OperationDefinitionNode
from typing import Any, List


class LazyVisitor(Visitor):
    """GraphQL syntax visitor to parse mutations into useful JSON/dicts"""

    # create a matcher for the operation+type info
    _action_parser = re.compile("^(" + "|".join(str(a) for a in Action) + ")(.*)$")

    def __init__(self):
        self.decoded = {}

    def enter_operation_definition(self, node: OperationDefinitionNode, *_args):
        """For all operations, accumulate the query + arguments as python dictionaries"""
        for selection in node.selection_set.selections:
            if self.decoded.get(node.name.value):
                self.decoded[node.name.value][selection.name.value] = self._args_to_dict(selection.arguments)
            else:
                self.decoded[node.name.value] = {selection.name.value: self._args_to_dict(selection.arguments)}
        return visitor.SKIP

    def _args_to_dict(self, args: List[ArgumentNode]):
        return {arg.name.value: graphql.value_from_ast_untyped(arg.value) for arg in args}

    @classmethod
    def parse_mutations(cls, mutations: List[str]):
        """Convert a list of mutation strings into dictionary types and provide them via an iterator

        This will automatically add a `mutation m` wrapper if one is not already present"""
        for mut in mutations:
            mutation = mut if mut.strip().startswith("mutation m") else "mutation m {" + mut + "}"
            ast = graphql.parse(graphql.Source(mutation, "GraphQL request"))
            argument_decoder = cls()
            visitor.visit(ast, argument_decoder)
            for operation, arguments in argument_decoder.decoded["m"].items():
                op, user_type = cls._action_parser.match(operation).groups()
                yield {"__operation": op, "__typename": user_type, "arguments": arguments}


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
