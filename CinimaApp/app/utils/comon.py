from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from datetime import date ,timedelta
from app.list.list_searhc import list_serach_name_title,list_serach_rating
YEARS_FILMS = 30 
YEARS_ACTOR = 80
async def is_name_title(model,session,name_filed,name_or_title_value)->bool:
    smt = select(model).where(getattr(model,name_filed)==name_or_title_value)
    relut = await session.execute(smt)
    extit =  relut.scalars().first() is None
    return extit
async def is_fistname_lastname(mode,session,dict_data):
    fields = list_serach_name_title[:3]
    mas = [getattr(mode,field)==dict_data[field] for field in fields]
    smt = select(mode).where(and_(*mas))
    relut = await session.execute(smt)
    extit =  relut.scalars().first() is None
    return extit
async def validate_is_data_range(value:date,type_obj:str)->bool:
    today = date.today()
    if type_obj == "film":
        min_date = today-timedelta(YEARS_FILMS*365)
        if value > today or value <min_date:
            return False
    elif type_obj=="actor"or type_obj=="author":
        min_date = today - timedelta(YEARS_ACTOR*365)
        if value > today or value <= min_date:
            return False
    return True
async def validet_star_rating(dict:dict,filed_name:str):
    if  filed_name == list_serach_rating[0]:
        if dict[filed_name] <=1 or dict[filed_name] >=10:
            return False
        return True
    elif  filed_name == list_serach_rating[1] :
        if dict[filed_name]<= 1 or dict[filed_name] >= 10:
            return False
        return True
    return False

