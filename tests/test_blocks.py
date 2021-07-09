import pytest
from vendia import blocks

sample_mutations = [
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

def test_type_of_returned_data():
    # Ensure parse_mutations returns a list
    data = blocks.parse_mutations(sample_mutations)
    assert type(data) is list

def test_quantity_of_items_in_returned_data():
    # Ensure data contains two objects
    data = blocks.parse_mutations(sample_mutations)
    assert len(data) == 2

def test_types_of_items_in_returned_data():
    # Make sure objects in the list are dicts
    data = blocks.parse_mutations(sample_mutations)
    for m in data:
        assert type(m) is dict

def test_keys_of_first_item_in_returned_data():
    # Make sure keys of the first item are set
    data = blocks.parse_mutations(sample_mutations)
    assert list(data[0].keys()) == ['operation', '__typename', 'arguments']

def test_input_dict_of_first_item_in_returned_data():
    data = blocks.parse_mutations(sample_mutations)



