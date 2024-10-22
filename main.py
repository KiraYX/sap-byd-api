# Update recently updated materials
import requests
from api.sap.material import fetch_recent_updated_data
from flow.sync.material_sync import sync_recently_updated_materials

with requests.Session() as session:
    material_data_list = fetch_recent_updated_data(session) 
sync_recently_updated_materials(material_data_list)