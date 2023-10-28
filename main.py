from fastapi import FastAPI
import uvicorn
from trainer.api.view.index_view import router as index_router
from trainer.api.view.data_view import router as data_router
from trainer.api.view.finetune_view import router as finetune_router
from trainer.api.view.merge_view import router as merge_router
from trainer.api.view.eval_view import router as eval_router
from trainer.api.view.chat_view import router as chat_router
from trainer.api.view.script_view import router as script_router
from trainer.api.api_task import router as api_router
from trainer.api.api_model import router as api_model
from trainer.settings import Settings

app = FastAPI()
app.include_router(index_router)
app.include_router(data_router)
app.include_router(finetune_router)
app.include_router(merge_router)
app.include_router(eval_router)
app.include_router(chat_router)
app.include_router(script_router)
app.include_router(api_router)
app.include_router(api_model)
my_settings = Settings()


if __name__ == "__main__":
    print("init")

    # run
    uvicorn.run("main:app", host="0.0.0.0", port=my_settings.app_port, log_level=my_settings.app_log_level)
