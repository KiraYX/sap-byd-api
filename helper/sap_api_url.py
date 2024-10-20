from .sap_tenant import get_tenant_hostname

# Function to construct the SAP OData API URL
# Designed for only one criteria filter typical ID
def construct_sap_odata_url(params):

    # Use the current active tenant
    tenant_hostname = get_tenant_hostname()
    
    # Extract parameters from the dictionary
    odata_service = params.get("odata_service")
    entity_set = params.get("entity_set")
    select = params.get("select", "")
    expand = params.get("expand", "")
    filter_property = params.get("filter_property", "")
    filter_operator = params.get("filter_operator", "eq")
    filter_value = params.get("filter_value", "")
    sap_language = params.get("sap-language", "ZH")

    # Construct base query
    query = f"{odata_service}/{entity_set}?"

    # Conditionally append $select if it's not empty
    if select:
        query += f"$select={select}&"

    # Conditionally append $expand if it's not empty
    if expand:
        query += f"$expand={expand}&"

    # Conditionally append $filter if filter_property and filter_value are provided
    if filter_property and filter_value:
        query += f"$filter={filter_property} {filter_operator} {filter_value}&"

    # Append sap-language
    query += f"sap-language={sap_language}&"

    # Append format as JSON
    query += "$format=json"

    # Return the complete URL
    return f"https://{tenant_hostname}/sap/byd/odata/cust/v1/{query}"

if __name__ == "__main__":

    params = {
        "odata_service": "mcmaterial",
        "entity_set": "MaterialCollection",
        "sap-language": "ZH",
        "select": "MaterialID,ObjectID,MaterialDescription,InternalDescription_KUT",  # Example with multiple selections
        "expand": "",  # No expand
        "filter_property": "MaterialID",  # Filter property and value
        "filter_operator": "eq",
        "filter_value": "10000001"
    }

    # Construct and print the URL
    url = construct_sap_odata_url(params)
    print(url)
