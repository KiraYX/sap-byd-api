
if __name__ == '__main__':
    # Example SAP response
    sap_sap_material_data = [
        {
            "ObjectID": "00163E8BB9C41EDAA8AF9493BA5801D8",
            "MaterialID": "10000058",
            "InternalDescription_KUT": "终端固定件_PXC_CLIPFIX 35",
            "MaterialName": "终端固定件",
            "Brand": "PXC",
            "ModelNumber": "CLIPFIX 35",
            "MaterialDescription": "节点_PXC_CLIPFIX 35",
            "BaseMeasureUnitCode": "EA",
            "ProductCategoryInternalID": "1102",
            "ProductCategoryDescription": "外购物料"
        }
        # Add more entries if needed
    ]

    # Use single entry to test
    converted_output = convert_sap_material_to_jdy_format(sap_sap_material_data[0])

    # Print the converted data using rich's print function
    rich_print(converted_output)

    # Convert the SAP response
    # converted_output = batch_convert_material_sap_to_jdy(sap_sap_material_data)

    # # Print the converted data using rich's print function
    # rich_print(converted_output)

    # Test jdy to widget
    converted_output = convert_jdy_json_to_widget_format(converted_output)
    rich_print(converted_output)
