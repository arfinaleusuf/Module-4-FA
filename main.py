from fastapi import FastAPI, Path, HTTPException, Body, Query
import json

app = FastAPI()

@app.get("/books")
def books():
    data = load_all()
    return data


def load_all():
    with open('library.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('library.json','w') as f:
        json.dump(data,f)

@app.get("/books/{book_id}")
def book_by_id(book_id: str = Path(..., deprecated="Give a valid book id",example="1")):
    data = load_all()

    if book_id in data:
        return data[book_id]
    else:
        raise HTTPException(status_code=404,detail="book not found")

@app.post("/add")
def add_book(book: dict = Body()):
    book_id = book["id"]

    data = load_all()

    data[book_id] = book
    del data[book_id]["id"]

    save_data(data)
    return "Successfully book added"

@app.get("/sort")
def soted_by(sorted_by: str = Query(default=...,description="sort on the basis of pages and rating",example=""), order: str = Query(default="asc",description="Select between asc and desc")):
    valid = ["pages", "rating"]
    data = load_all()

    if sorted_by not in valid:
        raise HTTPException(status_code=404, detail=f"invalid fields select from{valid}")
    if order not in["asc", "desc"]:
        raise HTTPException(status_code=404, detail="Select ace or desc")

    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by])
        return sorted_data
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x:x[sorted_by], reverse=True)
        return sorted_data