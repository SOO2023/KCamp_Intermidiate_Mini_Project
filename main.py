from fastapi import FastAPI
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
            },
        
}

class Book(BaseModel):
    title: str = Field(examples=["The Misterious Banana"])
    author:str = Field(examples=["John Doe"])
    publication_year:int = Field(examples=[1905])
    genre:list[str] = Field(examples=[["Novel", "Drama"]])


#Retrieve a list of books or just a book  
@app.get("/books")
def get_book(id: int | None = None):
    #if no id, return all books in collection
    if id is None:
        return books_db
    else:
        book_dict = books_db.get(id)
        #if book id does not exist, then return error message
        if book_dict is None:
            return {"error": f"This book id '{id}' does not exist in the book respository"}
        
        #if book id exists, then return book with id detail
        else:
            return {"id": id, "book_detail": book_dict}

#Create a new book
@app.post("/add_book")
def add_book(book_detail: Book):
    id = id_gen(books_db)
    new_book_dict = book_detail.model_dump()
    books_db[id] = new_book_dict
    title = book_detail.model_dump()["title"]
    return {"message": f"{title} was successfully added!",
            "book_detail":new_book_dict}

#Update detail of an existing book with a given id
@app.put("/book_update/{id}")
def update_book(id: int, book_detail: Book):
    old_book_dict = books_db.get(id)
    
    #if book id does not exist, return error message
    if old_book_dict is None:
        return {"error": f"This book id '{id}' does not exist in the book respository."}
    
    #if book id exists, update the detail
    else:
        new_book_dict = book_detail.model_dump()
        books_db[id] = new_book_dict
        return {"message":f"The book with id {id} was successfully updated!",
                "new_book_detail": new_book_dict,
                "old_book_detail": old_book_dict}

#Delete a book with a given id       
@app.delete("/book_delete/{id}")
def update_book(id: int):
    book_dict = books_db.get(id)
    
    #if book id does not exist, return error message
    if book_dict is None:
        return {"error": f"This book id '{id}' does not exist in the book respository."}
    
    #if id exists, delete book from respository
    else:
        del books_db[id]
        return {"message": f"The book with id {id} was successfully deleted from respository.",
                "deleted_book_detail":book_dict}
        