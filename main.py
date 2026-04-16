from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "hello my first firstapi"}