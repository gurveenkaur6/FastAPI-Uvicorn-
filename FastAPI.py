# Traditionally, you don't set what type of data your API endpoint is going to expect.
# You need yo do some data validation like checking if you got a JSON object, int, string etc.
# In FAST API, this is already done for you and if you send an object with wrong datatype, it will send an error to you.
# offers automatic data validation, automatic documentation.


# pip install uvicorn - uvicorn is used to run the API, its like a web server.

from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

# Initialise our api
app = FastAPI()

# Similar to a struct in C
class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class Update_Item(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


# endpoint/route - Base server URL. Each endpoint leads you to a different webpage having different context.
@app.get("/")
# Information returned when you go this endpoint
def home():
    # FastAPI also handles jsonifying all of our info that is being exchanged between you and the api.
    return {"Data" : "Test"}
# To run the API, uvicorn FastAPI:app --reload
# /docs will show the requests and data validation.


@app.get("/about")
def about():
    return {"Data" : "About"}

# Path and Query Parameters
# setting up an endpoint for an item in the inventory based on its id
# inventory = {
#     1 : {
#         "name": "Apple",
#         "price": 0.50,
#         "brand": "Organic farms"
#     },
#     2 : {
#         "name": "Poptart",
#         "price": 3.50,
#         "brand": "Poptarts original"
#     }
# }

# initialise the inventory to create new items in it.
inventory= {}


# item_id is the path param
@app.get("/get-item/{item_id}")
# mentioning the data type so that fastapi can auto validate. If a user enters wrong data type(eg: apple), then error message pops up.
# Path parameter: default id = None, extra desc about what to pass in the path)
def get_item(item_id: int = Path(description="The ID of the item you want to view")):
    return inventory[item_id]


# Query Parameters(SYNTAX: "?<variable_name1> = <value1>&<variable_name2> = <value2>")
@app.get("/get-by-name")
# name is the query param that the endpoint will accept.
def get_item(*, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not Found"}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Item name not found")


# We can't call this endpoint without having the query parameter - name. we get an error!
# To make a query parameter an optional query param, just set name : str = None(default) or just use name : Optional[str] = None
# * to avoid the python error for putting an non-optional param after an optional param.


# combining path and query params
@app.get("/get-by-name{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not Found"}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)


# Request Body - To send info to your database/inventory.
@app.post("/create-item/{item_id}")
# Putting a class as a parameter tells the FastAPI that this is for the request body and not a query param.
# item_id is the path param.
def create_item(item_id: int, item: Item):
    # take the item and insert it into the inventory.
    if item_id in inventory:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail = "Item ID already exists.")
    
    # inventory[item_id]= {"name" : item.name,"price": item.price , "brand" : item.brand}
    
    inventory[item_id]=item # fastapi will jsoinfy it automatically
    return inventory[item_id]

# item we just added was gone as soon as the server reloaded.


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Update_Item):
    if item_id not in inventory:
        raise HTTPException(status_code= 404, detail = "Item ID does not exist.")
    
    if item.name is not None:
        inventory[item_id].name = item.name
    if item.price is not None:
        inventory[item_id].price = item.price
    if item.brand is not None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(description= "The ID of the tem to be deleted")):
    if item_id not in inventory:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Item ID does not exist.")
    del inventory[item_id]
    return {"Success": "Item Deleted !"}

# a status code is returned whenever you call an http method. 
# default = 200 (OK), 201, 404 (Not found.

# How to return an error status code
# 1. from FastAPI import HTTPException, status
# 2. where you want to return some error msg, instead raise exception with a status code.