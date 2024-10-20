from rich import print as rich_print

# Field Mapping
MATERIAL_FIELD_MAPPING = {
    "ObjectID": "_widget_1728702222839",
    "InternalID": "_widget_1719911600379",
    "InternalDescription_KUT": "_widget_1719911600393",
    "Description": "_widget_1719911600380",
    "MaterialName": "_widget_1719911600381",
    "Brand": "_widget_1719911600382",
    "ModelNumber": "_widget_1719911600383"
}

# Function to convert SAP response to the desired structure
def convert_sap_response_to_widget_format(sap_response):
    converted_data = []

    # Loop through each result in the SAP response
    for result in sap_response:
        item_converted = {}

        # Loop through the MATERIAL_FIELD_MAPPING
        for field, widget_id in MATERIAL_FIELD_MAPPING.items():
            if field in result:  # Check if the field exists in the result
                item_converted[widget_id] = {'value': result[field]}

        if item_converted:  # Only add to converted_data if item_converted is not empty
            converted_data.append(item_converted)

    return converted_data

if __name__ == '__main__':
    # Example SAP response
    sap_response = [
        {
            "__metadata": {
                "uri": "https://my601274.sapbyd.cn/sap/byd/odata/cust/v1/mcmaterial/MaterialCollection('00163E8BB9C41EDAA8AF9493BA5801D8')",
                "type": "cust.Material"
            },
            "ObjectID": "00163E8BB9C41EDAA8AF9493BA5801D8",
            "MaterialID": "10000058",
            "LastChangeDateTime": "/Date(1728982792596)/",
            "InternalDescription_KUT": "终端固定件_PXC_CLIPFIX 35",
            "IsObsolete_KUT": False,
            "MaterialDescription": "节点_PXC_CLIPFIX 35",
            "MaterialDescriptionLanguageCode": "ZH",
            "BaseMeasureUnitCode": "EA",
            "ProductCategoryInternalID": "1102",
            "ProductCategoryDescription": "外购物料",
            "ProductCategoryLanguageCode": "ZH",
            "MaterialName": "终端固定件",
            "Brand": "PXC",
            "ModelNumber": "CLIPFIX 35"
        }
        # You can add more items to this list to handle multiple SAP response items
    ]

    # Convert the SAP response
    converted_output = convert_sap_response_to_widget_format(sap_response)

    # Print the converted data using rich's print function
    rich_print(converted_output)