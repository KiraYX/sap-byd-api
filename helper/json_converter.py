from rich import print as rich_print
from conf.field_mapping import MATERIAL_FIELD_MAPPING_JDY_TO_WIDGET, MATERIAL_FIELD_MAPPING_SAP_TO_JDY

# Function to convert a single SAP entry to JDY format
def convert_sap_material_to_jdy_format(sap_single_data, debug=False):
    item_converted = {}

    # Remap fields based on MATERIAL_FIELD_MAPPING_SAP_TO_JDY
    for sap_field, jdy_field in MATERIAL_FIELD_MAPPING_SAP_TO_JDY.items():
        if sap_field in sap_single_data:  # Check if the SAP field exists in the entry
            item_converted[jdy_field] = sap_single_data[sap_field]

    if debug:
        rich_print("Converted data in JDY format: ", item_converted)
    
    return item_converted

# Function to convert a list of SAP entries to JDY format
def batch_convert_material_sap_to_jdy(sap_multiple_data, debug=False):
    converted_data = [
        convert_sap_material_to_jdy_format(entry, debug) 
        for entry in sap_multiple_data
        if convert_sap_material_to_jdy_format(entry, debug)
    ]
    
    if debug:
        rich_print("Converted data list in JDY format: ", converted_data)

    return converted_data

# Function to convert generic JSON data using a field mapping
def convert_jdy_json_to_widget_format(single_jdy_data, debug=False):
    
    # Check the input data
    if debug:
        rich_print("Input data: ", single_jdy_data)

    # Initialize an empty dictionary to store the converted data
    converted_data = {}

    # Loop through each key-value pair in the input data
    for field, value in single_jdy_data.items():
        # Check if the field has a mapping, and if so, map it, if not, skip it
        if field in MATERIAL_FIELD_MAPPING_JDY_TO_WIDGET:
            # Map the field to the corresponding widget ID
            widget_id = MATERIAL_FIELD_MAPPING_JDY_TO_WIDGET[field]
            converted_data[widget_id] = {"value": value}

    # Confirm the converted data
    if debug:
        rich_print("Converted data use for update: ", converted_data)
    
    # Return the converted data
    return converted_data

# Batch convert jdy data to widget format
def batch_convert_jdy_json_to_widget_format(jdy_multiple_data, debug=False):

    converted_data = [
        convert_jdy_json_to_widget_format(entry, debug) 
        for entry in jdy_multiple_data
        if convert_jdy_json_to_widget_format(entry, debug)
    ]

    if debug:
        rich_print("Converted data list in widget format: ", converted_data)

    return converted_data

# Main block for standalone execution or future usage as a module
if __name__ == "__main__":
    # Configure logger to display messages only if the script is executed as main

    sap_query_data = [
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

    # Convert the input data
    converted_to_jdy = batch_convert_material_sap_to_jdy(sap_query_data, debug=False)

    # Print the converted output
    rich_print("Converted from SAP to JDY: {}", converted_to_jdy)

    convert_for_edit = batch_convert_jdy_json_to_widget_format(converted_to_jdy, debug=False)

    # Print the converted output
    rich_print("Converted output: {}", convert_for_edit)
