from .sap_tenant import get_tenant_hostname

# Function to construct the SAP ODataAPI URL
# Designed for only one criteria filter typical ID
def construct_sap_odata_url(params):

    # Use the current active tenant
    tenant_hostname = get_tenant_hostname()
    # Extract parameters from the dictionary
    odata_service = params.get("odata_service")
    entity_set = params.get("entity_set")
    select = params.get("select")
    expand = params.get("expand")
    filter_property = params.get("filter_property")
    filter_operator = params.get("filter_operator", "eq")
    filter_value = params.get("filter_value")

    # Construct the query
    query = (
        f"{odata_service}/{entity_set}"
        f"?$select={select}&$expand={expand}&$filter={filter_property} {filter_operator} '{filter_value}'&$format=json"
    )

    # Return the complete URL
    return f"https://{tenant_hostname}/sap/byd/odata/cust/v1/{query}"

if __name__ == "__main__":

    params = {
        "odata_service": "mcmaterial",
        "entity_set": "MaterialCollection",
        "internal_id": "10000001",
        "select": (
            "InternalID,"
            "ObjectID,"
            "Description,"
            "InternalDescription_KUT"
        ),
        "expand": (
            ""
        ),
        "filter_property": "InternalID",
        "filter_operator": "eq",
        "filter_value": "10001001"
    }


    url = construct_sap_odata_url(params)
    print(url)
