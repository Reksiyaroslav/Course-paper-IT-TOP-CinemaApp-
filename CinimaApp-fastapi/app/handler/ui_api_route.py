from fastapi.templating import Jinja2Templates
from fastapi import Request,APIRouter
ui_router = APIRouter(prefix="/frondet",tags=["Визуал"])
teamlates = Jinja2Templates(directory="app/templates")
@ui_router.get("/")
def view_film(request:Request,film:dict) -> dict:   
    return teamlates.TemplateResponse(name="profilses.html",context={"request":request,"film":film})