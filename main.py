from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from api.sap.fetch_sap_material import fetch_recent_updated_data
from flow.sync.material_sync import sync_recently_updated_materials

# Function to run the job
def run_sync_job():
    with requests.Session() as session:
        recent_updated_materials_data = fetch_recent_updated_data(session)
    sync_recently_updated_materials(recent_updated_materials_data)
    print("Job executed successfully.")

# Initialize the scheduler
scheduler = BlockingScheduler()

# Schedule the job to run every 5 minutes
scheduler.add_job(run_sync_job, 'interval', minutes=1)

if __name__ == "__main__":
    print("Starting the scheduler...")
    scheduler.start()
