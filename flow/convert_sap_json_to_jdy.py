from rich import print as rich_print

# Field Mapping
MATERIAL_FIELD_MAPPING = {
    "ObjectID": "_widget_1728702222839",  # Mapping for ObjectID
    "InternalID": "_widget_1719911600379",  # Mapping for InternalID
    "InternalDescription_KUT": "_widget_1719911600393",  # Mapping for InternalDescription_KUT
    "Description": "_widget_1719911600380",  # Optional field if needed
    "MaterialName": "_widget_1719911600381",  # Mapping for MaterialName
    "Brand": "_widget_1719911600382",  # Mapping for Brand
    "ModelNumber": "_widget_1719911600383"  # Mapping for ModelNumber
}

# Function to convert SAP response to the desired structure
def convert_sap_response_to_widget_format(sap_response):
    converted_data = {}

    # Loop through each result in the SAP response
    for result in sap_response['d']['results']:
        item_converted = {}

        # Loop through the MATERIAL_FIELD_MAPPING
        for field, widget_id in MATERIAL_FIELD_MAPPING.items():
            if field in result:  # Check if the field exists in the result
                item_converted[widget_id] = {'value': result[field]}

        converted_data = item_converted  # Only one item in the results, so we can assign directly

    return converted_data

if __name__ == '__main__':
    # Example SAP response
    sap_response = {
        'd': {
            'results': [
                {
                    '__metadata': {
                        'uri': "https://my601188.sapbyd.cn/sap/byd/odata/cust/v1/mcmaterial/MaterialCollection('00163E8BB9C41EDAA7CDB7A490EB7FA9')",
                        'type': 'cust.Material'
                    },
                    'ObjectID': '00163E8BB9C41EDAA7CDB7A490EB7FA9',
                    'InternalID': '10000001',
                    'InternalDescription_KUT': '043-拆垛及混码-视觉控制器_MUJIN_MC9000-3DV-RS-LOGI',
                    'Description': '043-拆垛及混码-视觉控制器_MUJIN_MC9000-3DV-RS-LOGI',
                    'MaterialName': '043-拆垛及混码-视觉控制器',
                    'Brand': 'MUJIN',
                    'ModelNumber': 'MC9000-3DV-RS-LOGI'
                }
            ]
        }
    }

    # Convert the SAP response
    converted_output = convert_sap_response_to_widget_format(sap_response)

    # Print the converted data using rich's print function
    rich_print(converted_output)
