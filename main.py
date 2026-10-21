
from fastapi import FastAPI

app = FastAPI(
    title="DevOps Demo API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "DevOps Demo API",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
