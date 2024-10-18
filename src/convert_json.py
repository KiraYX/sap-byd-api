from config import MATERIAL_FIELD_MAPPING
from rich import print as rich_print

# Function to convert generic JSON data using a field mapping
def convert_json_for_modify(input_data):
    converted_data = {}

    # Loop through each item in the input data
    for item in input_data['data']:
        item_converted = {}

        # Loop through each key-value pair in the item
        for field, value in item.items():
            widget_id = MATERIAL_FIELD_MAPPING.get(field)

            # If the field exists in the mapping, format it accordingly
            if widget_id:
                item_converted[widget_id] = {"value": value}

        # Assuming _id is the unique identifier for this item
        converted_data[item['_id']] = item_converted

    return converted_data

# Main block for standalone execution or future usage as a module
if __name__ == "__main__":
    input_data = {
        'data': [
            {
                'material_id': '10000001',
                'internal_description': '043-拆垛及混码-视觉控制器_MUJIN_MC9000-3DV-RS-LOGI',
                'material_name': '043-拆垛及混码-视觉控制器',
                'brand': 'MUJIN',
                'model_number': 'MC9000-3DV-RS-LOGI',
                '_id': '6683e2b3f99e5bc64e8b431d',
                'appId': '6683c4a2399857dff128b206',
                'entryId': '6683c4b0ae4fd18278021f46'
            }
        ]
    }

    # Convert the input data
    converted_output = convert_json_for_modify(input_data)
    
    # Print the converted data using rich's print function
    rich_print(converted_output)
