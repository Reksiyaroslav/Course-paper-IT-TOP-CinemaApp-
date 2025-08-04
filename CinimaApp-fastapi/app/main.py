from fastapi import FastAPI
from app.handler.user_api_handler import user_router
from app.handler.film_api_handler import film_router
from app.handler.actor_api_handler import actor_router
from app.db.engine import create_tabel
import uvicorn

app = FastAPI(debug=1)
app.include_router(user_router)
app.include_router(film_router)
app.include_router(actor_router)


@app.on_event("startup")
async def event():
    await create_tabel()


@app.get("/curent")
def hello_people() -> dict:
    return {"message": "Hello man or women my api"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=90, reload=True)
