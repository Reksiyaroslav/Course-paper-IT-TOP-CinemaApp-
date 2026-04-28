from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from app.handler.user_api_handler import user_router
from app.handler.film_api_handler import film_router
from app.handler.actor_api_handler import actor_router
from app.handler.author_api_handler import author_router
from app.handler.coment_api_handler import coment_router
from app.handler.ratingfilm_handler import rating_router
from app.handler.ui_api_route import ui_router
from  app.handler.type_film_api_handler import type_film_router
from app.handler.country_api_handler import country_router
from app.handler.review_api_handler import review_router
# from app.db.engine import create_tabelS
# from app.utils.sricpt.py iimport seedn_


app = FastAPI(debug=True, title="FilmApp")
# @app.on_event("startup")
# async def event():
# await create_tabel()
app.add_middleware(
    SessionMiddleware,
    secret_key="radom_moler",
    max_age=3600,  # 1 час
    same_site="lax",
    https_only=False,
)
app.include_router(review_router)
app.include_router(user_router)
app.include_router(film_router)
app.include_router(actor_router)
app.include_router(author_router)
app.include_router(coment_router)
app.include_router(rating_router)
app.include_router(type_film_router)
app.include_router(country_router)
app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def hello_people(request: Request) -> RedirectResponse:
    return RedirectResponse(url=request.url_for("main_item",type_model="film"), status_code=303)


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    url = request.url_for("main_item",type_model="film")
    return RedirectResponse(url)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=90)
