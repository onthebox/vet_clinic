import time
from enum import Enum
from typing import Dict, List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', response_model=Dict[str, str], summary='Display Welcoming Text')
async def root() -> Dict[str, str]:
    """Display welcoming text"""
    return {"mesage": "Welcome to extremely cool vet clinic B-)"}


@app.post('/post', response_model=Dict[str, int], summary='Post Timestamp')
async def post_timestamp() -> Dict[int, int]:
    """Post current timestamp"""
    ts = int(time.time())
    idx = len(post_db) 
    post_db.append(Timestamp(id=idx, timestamp=ts))
    return {"id": idx, "timestamp": ts}


@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
async def get_dog_by_kind(kind: Union[str, None] = None) -> List[Dog]:
    """Get the dogs by their kind or get all the dogs from the database"""
    if kind:
        query_result = [doggy for doggy in dogs_db.values() if doggy.kind.value == kind.lower()]
    else:
        query_result = [doggy for doggy in dogs_db.values()]
    return query_result


@app.post('/dog', response_model=Dog, summary='Post New Dog')
async def create_new_dog(name: str, pk: int, kind: str) -> Dog:
    """Post new dog entry to the database"""
    if dogs_db.get(pk, False):
        raise HTTPException(status_code=409, detail="Dog with such primary key already exists.")

    try:
        dogs_db[pk] = Dog(name=name, pk=pk, kind=kind.lower())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"Invalid kind of a dog: {e}")

    return dogs_db[pk]


@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Primary Key')
def get_dog_by_pk(pk: int) -> Dog:
    """Get dog by its primary key"""
    query_dog = dogs_db.get(pk, [])

    return query_dog


@app.patch('/dog/{pk}', response_model=Dog, summary='Edit Existent Dog')
def patch_dog_by_pk(pk: int, name: str, kind: str) -> Dog:
    """Edit dog entry by primary key"""
    if not dogs_db.get(pk, False):
        raise HTTPException(status_code=409, detail="Dog with such primary key doesn't exist.")
    
    try:
        dogs_db[pk].name = name
        dogs_db[pk].kind = DogType(kind.lower())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f'Invalid kind of a dog: {e}')

    return dogs_db[pk]

