import uvicorn
from fastapi import FastAPI
from views import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("run:app", port=8230, host="0.0.0.0", reload=True)