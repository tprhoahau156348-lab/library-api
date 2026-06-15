from fastapi import FastAPI
from database.db_connection import create_tables
from routes import book_routes, member_routes, report_routes
from logger_config import logger

app = FastAPI(
    title="Library Management API",
    description="A RESTful API for managing library books, members, and borrowings.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    logger.info("Application is starting up...")
    try:
        create_tables()
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize database tables: {e}")

app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Library Management API. Go to /docs for Swagger documentation."}