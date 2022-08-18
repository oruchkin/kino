import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class Film_work:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.datetime
    file_path: str
    rating: float
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    
@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass
class Genre_Film_Work:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.datetime


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


@dataclass
class Person_Film_Work:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.datetime





# #example
# @dataclass
# class Movie:
#     # Обратите внимание: для каждого поля указан тип
#     title: str
#     description: str
#     # Ещё один бонус: в dataclass вы можете определить значение по умолчанию
#     rating: float = field(default=0.0)
#     id: uuid.UUID = field(default_factory=uuid.uuid4)

#     # Ключевое отличие от обычных классов: вам не требуется объявлять метод __init__!
#     # def __init__(self, title, description, id): сгенерируется автоматически под капотом
#     # и будет соответствовать атрибутам, объявленным вами в классе


# movie = Movie(title='movie', description='new movie', rating=0.0)
# #movie.ss = 2
# print(movie)
# print(type(movie))
# #Movie(title='movie', description='new movie', rating=0.0, id=UUID('6fe77164-1dfe-470d-a32d-071973759539'))

