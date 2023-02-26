from dotenv import load_dotenv
load_dotenv()

from src.api import app
import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")), log_level="info")