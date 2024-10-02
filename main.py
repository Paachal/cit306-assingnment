from fastapi import FastAPI, Form
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/formDB?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["formdb"]
collection = db["formdata"]

class FormData(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    address: str
    city: str
    state: str
    country: str
    zip: str
    comments: str

@app.get("/", response_class=HTMLResponse)
async def read_form():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    age: int = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    country: str = Form(...),
    zip: str = Form(...),
    comments: str = Form(...)
):
    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "age": age,
        "address": address,
        "city": city,
        "state": state,
        "country": country,
        "zip": zip,
        "comments": comments
    }
    collection.insert_one(form_data)
    return {"message": "Form submitted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
