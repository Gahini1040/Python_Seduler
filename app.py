from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Step 1: Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credi.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Shopify Customers").sheet1  # Use your actual sheet name

@app.route('/webhook/customer-delete', methods=['POST'])
def customer_delete():
    data = request.get_json()
    customer_id = str(data['id'])  # Shopify sends 'id' field on delete

    try:
        ids = sheet.col_values(1)  # First column with customer IDs
        if customer_id in ids:
            row_index = ids.index(customer_id) + 1  # gspread is 1-indexed
            sheet.delete_rows(row_index)
            return jsonify({"message": f"Deleted customer ID {customer_id} from sheet."}), 200
        else:
            return jsonify({"message": f"Customer ID {customer_id} not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
