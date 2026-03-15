from enum import Enum

class Role_User(Enum):
    User = "user"
    Author = "author"
    Actor = "actor"


class Type_Rec(Enum):
    Like = "like"
    UnLike = "unlike"
    Non_Rec = "not_rec"

