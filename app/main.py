# Add more routes, sessions, ???? 

from fastapi import FastAPI
from app.routes import vote

app = FastAPI(title="CollectiveVote - Test (mvp xd)")

app.include_router(vote.router, prefix="/vote", tags=["Votación"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a CollectiveVote"}
