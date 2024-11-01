# Update recently updated materials
import requests
from api.sap.fetch_sap_material import fetch_recent_updated_data
from flow.sync.material_sync import sync_recently_updated_materials

with requests.Session() as session:
    recent_updated_materials_data = fetch_recent_updated_data(session) 
sync_recently_updated_materials(recent_updated_materials_data)