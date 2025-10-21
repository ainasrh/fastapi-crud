from motor.motor_asyncio import AsyncIOMotorClient
import os 
from dotenv import load_dotenv
import certifi

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")


# connect to mongo db uri
client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

# communicate to databas
db = client[MONGO_DB]

def get_collection(name:str):
    return db[name]