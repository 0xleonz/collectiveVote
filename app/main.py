# Add more routes, sessions, ???? 

from fastapi import FastAPI
from app.routes import vote
from app.database import init_db

app = FastAPI(title="CollectiveVote - Test (mvp xd)")

app.include_router(vote.router, prefix="/vote", tags=["Votación"])

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a CollectiveVote"}
