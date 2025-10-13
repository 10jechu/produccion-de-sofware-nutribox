from fastapi import FastAPI
app = FastAPI(title="NutriBox API")
@app.get("/")
def health():
    return {"status": "ok"}
