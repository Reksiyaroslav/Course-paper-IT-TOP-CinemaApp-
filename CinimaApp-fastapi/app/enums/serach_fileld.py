from enum import Enum
class SerachFiled(Enum):
    Name = ("fistname", "lastname", "patronymic", "title", "username")
    Auth = ("password", "email")
    Rating = ("star", "avegas_rating")
    Date = ("release_date", "birth_date")
    Des = ("description",)
 