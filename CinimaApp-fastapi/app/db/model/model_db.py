import uuid
import datetime
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
    declared_attr,
)

from sqlalchemy import (
    Table,
    Column,
    DateTime,
    func,
    Integer,
    UniqueConstraint,
    UUID,
)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, unique=True, nullable=False, default=uuid.uuid4
    )


film_actor = Table(
    "film_actor",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True),
)
author_ciema = Table(
    "author_ciema",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)
user_film = Table(
    "fans_user",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)
"""""
user_frends = Table(
    "user_frends",
    AdvancedDeclarativeBase.metadata,
   Column("friend_id",ForeignKey("users.id"),primary_key= True),
    Column("user_id",ForeignKey("users.id"),primary_key=True)
)""" ""


class RatingFilm(Base):

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    film_id: Mapped[UUID] = mapped_column(ForeignKey("films.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(
        "User", back_populates="rating_users", lazy="selectin"
    )
    film: Mapped["Film"] = relationship(
        "Film", back_populates="rating_films", lazy="selectin"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Author(Base):

    fistname: Mapped[str]

    lastname: Mapped[str]

    birth_date: Mapped[datetime.date]

    patronymic: Mapped[str]

    bio: Mapped[str]

    films_authored: Mapped[list["Film"]] = relationship(
        secondary=author_ciema, back_populates="authors"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Coment(Base):

    description: Mapped[str]
    countheart: Mapped[int] = mapped_column(default=0)
    countdemon: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    film_id: Mapped[UUID] = mapped_column(ForeignKey("films.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[list["User"]] = relationship(
        "User", back_populates="coments", lazy="selectin"
    )
    film: Mapped[list["Film"]] = relationship(
        "Film", back_populates="coments", lazy="selectin"
    )


class Actor(Base):

    fistname: Mapped[str]

    lastname: Mapped[str]

    patronymic: Mapped[str]
    star: Mapped[int] = mapped_column(default=0)

    birth_date: Mapped[datetime.date]

    films_acted: Mapped[list["Film"]] = relationship(
        secondary=film_actor, back_populates="actors"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Film(Base):

    description: Mapped[str]

    title: Mapped[str]

    release_date: Mapped[datetime.date]

    authors: Mapped[list[Author]] = relationship(
        secondary=author_ciema, back_populates="films_authored", lazy="selectin"
    )

    actors: Mapped[list[Actor]] = relationship(
        secondary=film_actor, back_populates="films_acted", lazy="selectin"
    )
    estimation: Mapped[int]
    coments: Mapped[list[Coment]] = relationship(
        "Coment", back_populates="film", lazy="selectin"
    )
    rating_films: Mapped[list["RatingFilm"]] = relationship(
        "RatingFilm", back_populates="film", lazy="selectin"
    )
    fans: Mapped[list["User"]] = relationship(
        "User", secondary=user_film, back_populates="likefilms"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    path_image: Mapped[str] = mapped_column(nullable=True)


class User(Base):

    password: Mapped[str]

    username: Mapped[str]

    email: Mapped[str]
    datetimenow: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    coments: Mapped[list["Coment"]] = relationship(
        "Coment", back_populates="user", lazy="selectin"
    )
    rating_users: Mapped[list["RatingFilm"]] = relationship(
        "RatingFilm", back_populates="user", lazy="selectin"
    )
    """friends: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_frends,
        primaryjoin=foreign(user_frends.c.user_id) == id,
        secondaryjoin=foreign(user_frends.c.friend_id) == id,
        backref="friend_of",
        lazy="selectin"
    )"""

    likefilms: Mapped[list["Film"]] = relationship(
        back_populates="fans", secondary=user_film, lazy="selectin"
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
