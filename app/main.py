# Add more routes, sessions, ???? 

from fastapi import FastAPI
from app.routes import vote
from app.database import init_db
from app.routes import auth
app = FastAPI(title="CollectiveVote - Test (mvp x)")

app.include_router(vote.router, prefix="/vote", tags=["Votación"])
app.include_router(auth.router)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a CollectiveVote"}
