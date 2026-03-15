from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.handler.user_api_handler import user_router
from app.handler.film_api_handler import film_router, get_block_films
from app.handler.actor_api_handler import actor_router
from app.handler.author_api_handler import author_router
from app.handler.coment_api_handler import coment_router
from app.handler.ratingfilm_handler import rating_router
from app.handler.ui_api_route import ui_router, teamlates


# from app.db.engine import create_tabelS
# from app.utils.sricpt.py iimport seedn_
import uvicorn

app = FastAPI(debug=True, title="FilmApp")
app.include_router(user_router)
app.include_router(film_router)
app.include_router(actor_router)
app.include_router(author_router)
app.include_router(coment_router)
app.include_router(rating_router)
app.include_router(ui_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# @app.on_event("startup")
# async def event():
# await create_tabel()
app.add_middleware(SessionMiddleware,secret_key = "radom_moler")

@app.get("/")
def hello_people(reqest: Request) -> RedirectResponse:
    return RedirectResponse(url=reqest.url_for("main_film"), status_code=303)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=90)
