from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# MongoDB Atlas setup
MONGO_URI = "mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/formDB?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["formdb"]
collection = db["formdata"]

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

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
    return RedirectResponse(url="/", status_code=303)
