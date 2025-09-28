import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

def fetch_intel_products():
    url = "https://www.intel.com/content/www/us/en/products/sensors.html"  # Example URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.select('.product-listing .product'):
            try:
                name = item.select_one('.product-title').get_text(strip=True)
                desc = item.select_one('.product-description').get_text(strip=True)
            except Exception:
                name = desc = ''
            products.append({'Company': 'Intel', 'Name': name, 'Description': desc})
    except Exception as e:
        print(f"Error fetching Intel products: {e}")
    return pd.DataFrame(products)

def fetch_nxp_products():
    url = "https://www.nxp.com/products"  # Example URL, replace with actual NXP product page
    products = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.select('.product-listing .product'):
            try:
                name = item.select_one('.product-title').get_text(strip=True) if item.select_one('.product-title') else ''
                desc = item.select_one('.product-description').get_text(strip=True) if item.select_one('.product-description') else ''
            except Exception:
                name = desc = ''
            products.append({'Company': 'NXP', 'Name': name, 'Description': desc})
    except Exception as e:
        print(f"Error fetching NXP products: {e}")
    return pd.DataFrame(products)


def fetch_tsmc_products():
    url = "https://www.tsmc.com/english/dedicatedFoundry/services/productService"  # Example URL, replace with actual TSMC product page
    products = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.select('.product-listing .product'):
            try:
                name = item.select_one('.product-title').get_text(strip=True) if item.select_one('.product-title') else ''
                desc = item.select_one('.product-description').get_text(strip=True) if item.select_one('.product-description') else ''
            except Exception:
                name = desc = ''
            products.append({'Company': 'TSMC', 'Name': name, 'Description': desc})
    except Exception as e:
        print(f"Error fetching TSMC products: {e}")
    return pd.DataFrame(products)

class SuppliesDataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.csv_files = [
            "Intel_sensors_semiconductors_MCUs_full_dataset.csv",
            "NXP_sensors_and_MCUs_full_dataset.csv",
            "tsmc_merged_with_customer_datasheets.csv"
        ]

    def load_and_combine(self):
        """
        Loads and combines all product CSVs in the data folder.
        Returns a single DataFrame with all products.
        """
        dfs = []
        for csv_file in self.csv_files:
            path = os.path.join(self.data_dir, csv_file)
            if os.path.exists(path):
                df = pd.read_csv(path, encoding='utf-8', on_bad_lines='skip')
                dfs.append(df)
        if not dfs:
            raise FileNotFoundError("No data files found in data directory.")
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df

    def fetch_realtime_updates(self):
        """
        Fetches real-time product updates from Intel, NXP, and TSMC.
        Returns a DataFrame of new/updated products.
        """
        dfs = [
            fetch_intel_products(),
            fetch_nxp_products(),
            fetch_tsmc_products(),
        ]
        dfs = [df for df in dfs if not df.empty]
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        return pd.DataFrame()

    def get_up_to_date_products(self):
        """
        Returns a DataFrame with all products, including real-time updates.
        """
        combined_df = self.load_and_combine()
        realtime_df = self.fetch_realtime_updates()
        update_info_path = os.path.join(self.data_dir, 'update_info.json')
        update_history_path = os.path.join(self.data_dir, 'update_history.json')
        new_items_count = 0
        new_products = []
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not realtime_df.empty:
            # Find new products (not already in combined_df by Name and Company)
            if not combined_df.empty:
                merged = pd.merge(realtime_df, combined_df, on=["Name", "Company"], how="left", indicator=True)
                new_products_df = merged[merged["_merge"] == "left_only"][realtime_df.columns]
            else:
                new_products_df = realtime_df
            new_items_count = len(new_products_df)
            new_products = new_products_df.to_dict(orient="records")
            # Merge or update products as needed (customize merge logic as required)
            combined_df = pd.concat([combined_df, realtime_df], ignore_index=True)
        # Write update info (latest)
        update_info = {
            "last_update_time": update_time,
            "new_items_count": new_items_count,
            "new_products": new_products
        }
        try:
            with open(update_info_path, 'w', encoding='utf-8') as f:
                json.dump(update_info, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error writing update info: {e}")
        # Append to update history
        try:
            if os.path.exists(update_history_path):
                with open(update_history_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            history.append({
                "update_time": update_time,
                "new_items_count": new_items_count,
                "new_products": new_products
            })
            with open(update_history_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error writing update history: {e}")
        return combined_df