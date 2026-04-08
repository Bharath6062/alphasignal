import schedule 
import time 
import subprocess
import logging
from datetime import  datetime
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def run_pipeline():
    logging.info(f"Pipeline started at {(datetime.now())}")

    result = subprocess.run(["venv\\scripts\\python.exe" , "src/ingestion/fetch_prices.py"])
    if result.returncode != 0:
        logging.error("fetch_prices.py failed. Stopping pipeline.")
        return
    logging.info("fetch_prices.py completed successfully.")

    result = subprocess.run(["venv\\scripts\\python.exe", "src/ingestion/db_loader.py"])
    if result.returncode!=0:
        logging.error("db_loader.py is failed , pipeline stopped ")
        return
    logging.info("dbt_loader.py completed successfully")
    
    result = subprocess.run(["dbt","run","--project-dir","transforms"])
    if result.returncode!=0:
        logging.error("dbt failed , stopping pipeline ")
        return
    logging.info("dbt runned successfully")
    
logging.info(f"Pipeline completed successfully at {datetime.now()}")
    
schedule.every().day.at ("06:00").do (run_pipeline)
print ("scheduler running . pipeline everyday at 06:00.")

while True:
        schedule.run_pending()
        time.sleep(60)