import schedule
import time
from src.data_loader import SuppliesDataLoader

def update_products():
    loader = SuppliesDataLoader("data")
    df = loader.get_up_to_date_products()
    df.to_csv("data/combined_products.csv", index=False)
    print("Product data updated!")

schedule.every().day.at("02:00").do(update_products)  # Runs daily at 2 AM

while True:
    schedule.run_pending()
    time.sleep(60)