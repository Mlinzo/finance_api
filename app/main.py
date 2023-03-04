import config
from fastapi import FastAPI
from database.utils import init_db, fill_db, drop_db
from routes import plans_router, credits_router, other_router

app = FastAPI()

app.include_router(plans_router)
app.include_router(credits_router)
app.include_router(other_router)

@app.on_event("startup")
async def startup():
    # await drop_db()
    await init_db()
    await fill_db()