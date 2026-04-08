import schedule 
import time 
import os 
import subprocess
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import  datetime
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_alert(message: str):
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    
    msg = MIMEText(message)
    msg["Subject"] = "AlphaSignal Pipeline Alert"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
        logging.info("Alert email sent.")
    except Exception as e:
        logging.error(f"Failed to send alert email: {e}")


def run_pipeline():
    logging.info(f"Pipeline started at {(datetime.now())}")

    result = subprocess.run(["venv\\scripts\\python.exe" , "src/ingestion/fetch_prices.py"])
    if result.returncode != 0:
        logging.error("fetch_prices.py failed. Stopping pipeline.")
        send_alert("fetch_prices.py failed. Check logs for details.")
        return
    logging.info("fetch_prices.py completed successfully.")

    result = subprocess.run(["venv\\scripts\\python.exe", "src/ingestion/db_loader.py"])
    if result.returncode!=0:
        logging.error("db_loader.py is failed , pipeline stopped ")
        send_alert("db_loader.py failed , pipeline stopped ")
        return
    logging.info("dbt_loader.py completed successfully")
    
    result = subprocess.run(["dbt","run","--project-dir","transforms"])
    if result.returncode!=0:
        logging.error("dbt failed , stopping pipeline ")
        send_alert("dbt failed ,stopping pipeline")
        return
    logging.info("dbt runned successfully")
    logging.info(f"Pipeline completed successfully at {datetime.now()}")
    
schedule.every().day.at("06:00").do (run_pipeline)
print ("scheduler running . pipeline everyday at 06:00.")

while True:
        schedule.run_pending()
        time.sleep(60)