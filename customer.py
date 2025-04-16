import time
import schedule
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SHOP_URL, API_VERSION, ACCESS_TOKEN, CREDENTIALS_FILE

GOOGLE_SHEET_NAME = "Shopify Customer"

def fetch_and_update_customers():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1

    url = f"{SHOP_URL}/admin/api/{API_VERSION}/customers.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        customers_data = response.json().get("customers", [])
        if not customers_data:
            print("⚠️ No customer data found.")
        else:
            print(f"✅ Found {len(customers_data)} customers. Updating sheet...")
            sheet.clear()
            headers_row = list(customers_data[0].keys())
            sheet.append_row(headers_row)
            for customer in customers_data:
                row = [str(customer.get(col, "")) for col in headers_row]
                sheet.append_row(row)
            print("✅ Google Sheet updated successfully!")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

# === Schedule the function every 10 minutes (for example) ===
schedule.every(10).minutes.do(fetch_and_update_customers)

print("⏳ Scheduler started. Waiting for the next run...")

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    fetch_and_update_customers()
