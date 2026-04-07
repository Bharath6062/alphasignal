import schedule 
import time 
import subprocess
from datetime import  datetime

def run_pipeline():
    print(f"Pipeline started at {(datetime.now())}")
    subprocess.run(["python", "src/ingestion/fetch_prices.py"])
    subprocess.run(["python", "src/ingestion/db_loader.py"])
    subprocess.run(["dbt","run","--project-dir","transforms"])
    
schedule.every().day.at ("06:00").do (run_pipeline)
print ("scheduler running . pipeline everyday at 06:00.")

while True:
        schedule.run_pending()
        time.sleep(60)