from fastapi import FastAPI
from app.routers import auth, project, billing_generation, billing_history,company
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://billflow.addnectarstudio.com"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(company.router)
app.include_router(project.router)
app.include_router(billing_generation.router)
app.include_router(billing_history.router)