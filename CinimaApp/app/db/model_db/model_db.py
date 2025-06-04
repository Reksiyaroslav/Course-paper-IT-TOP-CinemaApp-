from uuid import UUID
import datetime
from sqlalchemy import ForeignKey,UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship,declarative_base
from litestar.plugins.sqlalchemy import base
from sqlalchemy import Table,Column,DateTime,func
from sqlalchemy import MetaData
from advanced_alchemy.base import AdvancedDeclarativeBase

film_actor = Table(

    "film_actor",
    AdvancedDeclarativeBase.metadata,
    Column("film_id", ForeignKey("cinemas.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True),
)
author_ciema = Table(

    "author_ciema",
    AdvancedDeclarativeBase.metadata,
    Column("film_id", ForeignKey("cinemas.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Author(base.UUIDBase):
    __tablename__ = "authors"
 
    fistName:Mapped[str]

    lastName:Mapped[str]

    birth_date:Mapped[datetime.datetime] = mapped_column(DateTime, default= datetime.datetime.now)

    patronymic:Mapped[str]

    bio:Mapped[str]

    films_authored:Mapped[list["Film"]] =relationship(secondary=author_ciema,back_populates="authors")


class Actor(base.UUIDBase):
    __tablename__ = "actors"

    fistName:Mapped[str]

    lastName:Mapped[str]

    patronymic:Mapped[str]
    star:Mapped[int] = mapped_column(default=0)
    
    birth_date:Mapped[datetime.datetime] = mapped_column(DateTime, default= datetime.datetime.now(datetime.timezone.utc))

    films_acted:Mapped[list["Film"]] =relationship(secondary=film_actor,back_populates="actors")

class Film(base.UUIDAuditBase):
    __tablename__ = "cinemas"
    
    description:Mapped[str] 

    title:Mapped[str] 

    release_date:Mapped[datetime.date]  

    estimation:Mapped[int] 

    authors:Mapped[list[Author]] =  relationship(secondary=author_ciema,back_populates="films_authored",lazy= "selectin")

    actors:Mapped[list[Actor]] = relationship(secondary=film_actor,back_populates="films_acted",lazy= "selectin")

class User(base.UUIDBase):
    __tablename__ = "users"
    
    password:Mapped[str] 

    username:Mapped[str] 

    email:Mapped[ str]

    datetimenow:Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(datetime.timezone.utc))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


  
    


    