from fastapi import FastAPI
import uvicorn
from apis.index_view import router as index_router
from apis.data_view import router as data_router
from apis.finetune_view import router as finetune_router
from apis.merge_view import router as merge_router
from apis.chat_view import router as chat_router
from apis.script_view import router as script_router
from apis.api import router as api_router

app = FastAPI()
app.include_router(index_router)
app.include_router(data_router)
app.include_router(finetune_router)
app.include_router(merge_router)
app.include_router(chat_router)
app.include_router(script_router)
app.include_router(api_router)


if __name__ == "__main__":
    print("init")

    # run
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
