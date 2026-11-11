from fastapi import FastAPI
from backend.articles import router_articles

app = FastAPI()

app.include_router(router_articles)