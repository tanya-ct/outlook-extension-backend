from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import email
from app.database import engine, Base
from app.routes import auth 
from app.routes.email import router as email_router

# Optional: create tables (in dev only — use Alembic in prod)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Outlook Email Backend",
    version="1.0.0"
)

# CORS Middleware (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(email.router, prefix="/api", tags=["Emails"])
app.include_router(auth.router)
app.include_router(email_router) 


@app.get("/")
def root():
    return {"status": "ok", "message": "Email backend is running."}
