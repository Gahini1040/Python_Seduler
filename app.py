# app.py

from flask import Flask, request
from utils import get_gsheet_client
from config import GOOGLE_SHEET_NAME

app = Flask(__name__)

@app.route("/webhook/customers/delete", methods=["POST"])
def handle_customer_delete():
    data = request.get_json()
    customer_id = str(data.get("id"))

    print(f"🗑️ Received deletion webhook for customer ID: {customer_id}")

    try:
        client = get_gsheet_client()
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        all_data = sheet.get_all_values()
        headers = all_data[0]

        if "id" not in headers:
            return "❌ 'id' column not found", 400

        id_col_index = headers.index("id") + 1

        for row_num, row in enumerate(all_data[1:], start=2):
            if row[id_col_index - 1] == customer_id:
                sheet.delete_rows(row_num)
                print(f"✅ Deleted row {row_num} for customer ID {customer_id}")
                return "✔️ Row deleted", 200

        print("⚠️ Customer ID not found in sheet.")
        return "Not Found", 404

    except Exception as e:
        print(f"❌ Error: {e}")
        return "Internal Error", 500

if __name__ == "__main__":
    app.run(port=5000)
