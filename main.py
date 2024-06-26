from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from helper_fun import id_gen

app = FastAPI()


books_db = {
            1:{
                "title":"Don Quixote",
                "author":"Miguel de Cervantes",
                "publication year":2018,
                "genre":["Novel", "Parody", "Satire"]
            },
            
            2:{
                "title":"Alice's Adventures in Wonderland",
                "author":"Lewis Carroll",
                "publication year":2017,
                "genre":["Fantasy Fiction", "Literary Nonsense"]
            },

            3:{
                "title":"The Adventures of Huckleberry Finn",
                "author":"Mark Twain",
                "publication year":2001,
                "genre":["Novel", "Satire", "Adventure fiction"]
            },

            4:{
                "title":"Pride and Prejuice",
                "author":"Jane Austin",
                "publication year":2017,
                "genre":["Romance Novel", "Drama", "Historical Fiction"]
            },

            5:{
                "title":"Treasure Island",
                "author":"Robert Louis Stevenson",
                "publication year":1981,
                "genre":["Novel", "Adventure Fiction"]
            }
        
}

id_generator = id_gen(len(books_db))

class Book(BaseModel):
    title: str = Field(examples=["The Mysterious Banana"])
    author:str = Field(examples=["John Doe"])
    publication_year:int = Field(examples=[1905])
    genre:list[str] = Field(examples=[["Novel", "Drama"]])


#Retrieve a list of books in the collection
@app.get("/books")
def get_books():
    return books_db

#Retrieve a book with a given id
@app.get("/books/{id}")
def get_book(id:int):
    book_dict = books_db.get(id)
    #if book id does not exist, then return error message
    if book_dict is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This book id '{id}' does not exist in the book respository.")
    
    #if book id exists, then return book with id detail
    else:
        return {"id": id, "book_detail": book_dict}

#Create a new book
@app.post("/add_book", status_code=status.HTTP_201_CREATED)
def add_book(book_detail: Book):
    id = next(id_generator)
    new_book_dict = book_detail.model_dump()
    books_db[id] = new_book_dict
    title = book_detail.model_dump()["title"]
    return {"message": f"{title} was successfully added!",
            "book_detail":new_book_dict}

#Update detail of an existing book with a given id
@app.put("/book_update/{id}", status_code=status.HTTP_201_CREATED)
def update_book(id: int, book_detail: Book):
    old_book_dict = books_db.get(id)
    
    #if book id does not exist, return error message
    if old_book_dict is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This book id '{id}' does not exist in the book respository.")
    
    #if book id exists, update the detail
    else:
        new_book_dict = book_detail.model_dump()
        books_db[id] = new_book_dict
        updates = {i: {"old":old_book_dict[i], "new":new_book_dict[i]} for i in old_book_dict.keys() if old_book_dict[i] != new_book_dict[i]}
        return {"message":f"The book with id {id} was successfully updated!",
                "updates":updates}

#Delete a book with a given id       
@app.delete("/book_delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_book(id: int):
    book_dict = books_db.get(id)
    
    #if book id does not exist, return error message
    if book_dict is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This book id '{id}' does not exist in the book respository.")
    
    #if id exists, delete book from respository
    else:
        del books_db[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
