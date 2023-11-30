from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Allow Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["a1"]

class Item(BaseModel):
    name: str
    description: str

@app.get("/api/health")
async def health_check():
    try:
        # Attempt to query the database to check the connection
        result = collection.find_one({})
        if result:
            return {"status": "OK"}
        else:
            raise HTTPException(status_code=500, detail="Database query failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking database connection: {str(e)}") 
    
@app.get("/api/health")
async def health_check():
    try:
        # Attempt to query the database to check the connection
        result = collection.find_one({})
        if result:
            return {"status": "OK"}
        else:
            raise HTTPException(status_code=500, detail="Database query failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking database connection: {str(e)}")

@app.post("/api/save_status")
async def create_item(item: Item):
    # Endpoint for the admin to post information to the database
    document = item.dict()
    result = collection.insert_one({"name":"abc"})
    print("post")
    return {"status": "Item posted successfully", "id": str(result.inserted_id)}

@app.get("/api/client/read/{item_id}")
async def read_item(item_id: str):
    # Endpoint for the client to read information from the database
    document = collection.find_one({"_id": item_id})
    if document:
        return document
    else:
        raise HTTPException(status_code=404, detail="Item not found")
