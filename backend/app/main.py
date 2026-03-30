from fastapi import FastAPI
from app.routes import traffic, gps, signals

app = FastAPI()

app.include_router(traffic.router, prefix="/traffic")
app.include_router(gps.router, prefix="/gps")
app.include_router(signals.router, prefix="/signals")

@app.get("/")
def root():
    return {"message": "Traffic System Running"}