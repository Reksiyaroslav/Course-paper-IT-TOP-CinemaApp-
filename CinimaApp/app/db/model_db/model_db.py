from uuid import UUID
import datetime
from sqlalchemy import ForeignKey,UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship,declarative_base
from litestar.plugins.sqlalchemy import base
from sqlalchemy import Table,Column,DateTime,func,Integer,UniqueConstraint
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
user_coment = Table(
    "user_coment",
    AdvancedDeclarativeBase.metadata,
    Column("user_id",ForeignKey("users.id"),primary_key=True ),
    Column("coment_id",ForeignKey("coments.id"),primary_key=True )
)
film_coment = Table(
    "film_coment",
    AdvancedDeclarativeBase.metadata,
    Column("film_id",ForeignKey("cinemas.id"),primary_key=True ),
    Column("coment_id",ForeignKey("coments.id"),primary_key=True )
)

class RatingFilm(base.UUIDBase):
    __tablename__ = "ratingfilms"
    __table_args__ = (UniqueConstraint("user_id", "film_id", name="uix_user_film"),)
    rating:Mapped[int] = mapped_column(Integer , nullable=False)
    film_id:Mapped[UUID] = mapped_column(ForeignKey("cinemas.id"),nullable=False)
    user_id:Mapped[UUID] = mapped_column(ForeignKey("users.id"),nullable=False)
    user:Mapped["User"] = relationship("User",back_populates="rating_users")
    film:Mapped["Film"] = relationship("Film",back_populates="rating_films")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Author(base.UUIDBase):
    __tablename__ = "authors"
 
    fistname:Mapped[str]

    lastname:Mapped[str]

    birth_date:Mapped[datetime.date] 

    patronymic:Mapped[str]

    bio:Mapped[str]

    films_authored:Mapped[list["Film"]] =relationship(secondary=author_ciema,back_populates="authors")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Coment(base.UUIDBase):
    __tablename__ = "coments"
    description:Mapped[str] 
    countheart:Mapped[int]
    countdemon:Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    users :Mapped[list["User"]] =relationship(secondary=user_coment,back_populates="coment_users",lazy= "selectin")
    films: Mapped[list["Film"]] =relationship(secondary=film_coment,back_populates="films_comnet",lazy= "selectin" )
    

class Actor(base.UUIDBase):
    __tablename__ = "actors"

    fistname:Mapped[str]

    lastname:Mapped[str]

    patronymic:Mapped[str]
    star:Mapped[int] = mapped_column(default=0)
    
    birth_date:Mapped[datetime.date] 

    films_acted:Mapped[list["Film"]] =relationship(secondary=film_actor,back_populates="actors")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    


class Film(base.UUIDAuditBase):
    __tablename__ = "cinemas"
    
    description:Mapped[str] 

    title:Mapped[str] 

    release_date:Mapped[datetime.date]  

    authors:Mapped[list[Author]] =  relationship(secondary=author_ciema,back_populates="films_authored",lazy= "selectin")

    actors:Mapped[list[Actor]] = relationship(secondary=film_actor,back_populates="films_acted",lazy= "selectin")
    estimation:Mapped[int]
    films_comnet:Mapped[list[Coment]] = relationship(secondary=film_coment,back_populates="films")
    rating_films :Mapped[list["RatingFilm"]] = relationship("RatingFilm",back_populates="film",lazy = "selectin")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

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
    coment_users:Mapped[list["Coment"]] =relationship(secondary=user_coment,back_populates="users")
    rating_users:Mapped[list["RatingFilm"]] = relationship("RatingFilm",back_populates="user")
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
