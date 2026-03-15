from typing import Dict,Any 
def text_strip_lower(text: str) -> str:
    if text is None:
        return ""
    return text.strip().lower()
def text_strip(text:str):
     if text is None:
          return ""
     return text.strip()
def no_change(value: Any) -> Any:
        return value
NORMAL_CONFING = {
        "actor":{"firstname":text_strip_lower,
                "lastname":text_strip_lower,
                "patronymic": text_strip_lower,
                "birth_date": no_change,
                "star": no_change,             
              
              },
        "author":{"firstname":text_strip_lower,
                "lastname":text_strip_lower,
                "patronymic": text_strip_lower,
                "birth_date": no_change,
                "bio": text_strip,             
              
              },
        "film":{
             "title":text_strip,
             "description":text_strip,
             "release_date":no_change
        },
        "user":{
             "username": text_strip_lower,
            "email": text_strip_lower,
            "password": no_change,
        },
}
def normalize_data(data:Dict[str,Any],model_type:str)->Dict[str,Any]:
     cofing = NORMAL_CONFING.get(model_type,{})
     if not cofing:
          return data
     return{
          field:normalize(data.get(field))
          for field,normalize in cofing.items()
     }

       