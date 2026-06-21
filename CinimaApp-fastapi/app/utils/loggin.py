from logging import FileHandler, Logger,getLogger,Handler,LogRecord,DEBUG,Formatter
from datetime import time,date,datetime
from re import sub,match
def get_login(name:str) -> Logger:
    log = getLogger(name)
    log.setLevel(DEBUG)
    py_filter = Formatter("%(name)s %(levelno)s  %(filename)s  %(asctime)s  %(message)s" )
    py_nadler = FileHandler(filename="log.log",encoding="utf-8",)
    py_nadler.setFormatter(py_filter)
    log.addHandler(py_nadler)
    return log
Pet_type = ["cat","dog"]
str = "cat"
date_today:date = date.today()

print(str in Pet_type)
str_number = "+7 (930) 71-22-192"
str = "1"
clen_number = sub(r"[\s\-\(\)]","",str_number)
print(clen_number)
str_nuber = r"^(8|\+7)\d{10}$"

str_strng_paterrn = r"^[A-Za-zА-Яа-я-0-9]+$"
print(bool(match(str_strng_paterrn,str)))
bool_number = bool(match(str_nuber,clen_number))
print(bool_number)

