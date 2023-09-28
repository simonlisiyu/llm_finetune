from typing import Union

from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
# run app
# uvicorn main:app --reload


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})


@app.post("/bar")
async def read_item(
        foo: int = Body(1, title='描述', embed=True),
        age: int = Body(..., le=120, title="年龄", embed=True),
        name: str = Body(..., regex="^xiao\d+$", embed=True)
):
    print(foo, age, name)
    query = "保暖的大衣"

    return {"foo": foo, "age": age, "name": name}


@app.post("/add_document")
async def add_document_endpoint(item: Item):
    print("add_document end.")
    return {"message": "Document added successfully", "data": item}


@app.post("/search_documents")
async def search_documents_endpoint(query: str = Body(..., title='请求文本', embed=True),
                                    num: int = Body(..., le=120, title="返回数量", embed=True)):
    print(query, num)
    return {"message": "Query searched successfully", "data": "12"}

if __name__ == "__main__":
    ## init
    print("init")

    # run
    uvicorn.run("main:app", host="0.0.0.0", port=8000)