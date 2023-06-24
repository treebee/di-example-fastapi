from fastapi import FastAPI


app = FastAPI(title="Hello Karlsruhe Python Meetup", version="2023.07.12")


from .routers.offers import router as offers_router

app.include_router(offers_router)
