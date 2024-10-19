from conf.config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, SAP_TENANT_ACTIVE

# Decide the tenant by argument or by active tenant
def get_tenant_hostname(tenant=None):
    # If tenant is None, use the current active tenant
    if tenant is None:
        tenant = SAP_TENANT_ACTIVE  # Use the current active tenant

    # Determine the tenant hostname based on the provided tenant
    tenant_hostname = SAP_PROD_TENANT_HOSTNAME if tenant == 'prod' else SAP_TEST_TENANT_HOSTNAME
    return tenant_hostname

# Main function to test
if __name__ == "__main__":
    active_hostname = get_tenant_hostname()
    print("tenant hostname determined:",active_hostname)