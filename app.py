import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify

app = Flask(__name__)

GOOGLE_SHEET_NAME = "Testing customer"  # Change this to your Google Sheet name
LAST_ROW_TRACKING_CELL = "Z1"  # Cell to track the last processed customer ID

def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credi.json", scope)
    return gspread.authorize(creds)

@app.route('/webhook', methods=['POST'])
def customer_deleted():
    # Shopify sends the customer's ID in the webhook when a customer is deleted
    data = request.json
    customer_id = data.get('id')

    if customer_id:
        print(f"❌ Customer {customer_id} deleted from Shopify. Removing from Google Sheet...")
        remove_customer_from_sheet(customer_id)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Invalid webhook data"}), 400

def remove_customer_from_sheet(customer_id):
    client = get_gsheet_client()
    try:
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Spreadsheet '{GOOGLE_SHEET_NAME}' not found or not shared with the service account.")
        return

    # Find the customer row based on ID
    all_values = sheet.get_all_values()
    headers = all_values[0]  # First row should be the header row
    customer_id_col_index = headers.index("id")  # Assuming "id" is the first column header

    # Find the customer row to delete
    for row_index, row in enumerate(all_values[1:], start=2):  # Skip header
        if int(row[customer_id_col_index]) == customer_id:
            # Delete the row
            sheet.delete_rows(row_index)
            print(f"✅ Customer {customer_id} removed from Google Sheet.")
            return

    print(f"❌ Customer {customer_id} not found in Google Sheet.")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
