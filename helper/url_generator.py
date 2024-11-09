from conf.config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, SAP_TENANT_ACTIVE

# Decide the tenant by argument or by active tenant
def get_tenant_hostname(tenant=None):
    # If tenant is None, use the current active tenant
    if tenant is None:
        tenant = SAP_TENANT_ACTIVE  # Use the current active tenant

    # Determine the tenant hostname based on the provided tenant
    tenant_hostname = SAP_PROD_TENANT_HOSTNAME if tenant == 'prod' else SAP_TEST_TENANT_HOSTNAME
    return tenant_hostname

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

    query_url = f"https://{tenant_hostname}/sap/byd/odata/cust/v1/{query}"
    print("Query URL:", query_url)

    # Return the complete URL
    return query_url

if __name__ == "__main__":

    # Import only for testing
    from loguru import logger

    # Decide tenant by global variable
    active_hostname = get_tenant_hostname()

    print("tenant hostname determined:", active_hostname)
    # Use logger to print the tenant hostname
    logger.debug("tenant hostname determined: {active_hostname}", active_hostname=active_hostname)

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

    # Use logger to print the URL
    logger.debug(url)
