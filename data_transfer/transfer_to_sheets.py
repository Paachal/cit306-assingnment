import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pymongo import MongoClient

# MongoDB Atlas setup
MONGO_URI = "mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/formDB?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["formdb"]
collection = db["formdata"]

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'data_transfer/service-account-file.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of the spreadsheet.
SPREADSHEET_ID = 'cit-306-437407'
RANGE_NAME = 'Sheet1!A1:J11'  # Adjust the range as needed

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Fetch data from MongoDB
data = collection.find()
values = [["Name", "Email", "Phone", "Age", "Address", "City", "State", "Country", "Zip", "Comments"]]

for entry in data:
    values.append([
        entry.get("name"),
        entry.get("email"),
        entry.get("phone"),
        entry.get("age"),
        entry.get("address"),
        entry.get("city"),
        entry.get("state"),
        entry.get("country"),
        entry.get("zip"),
        entry.get("comments")
    ])

# Write data to Google Sheets
body = {
    'values': values
}

result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
    valueInputOption="RAW", body=body).execute()

print(f"{result.get('updatedCells')} cells updated.")
