from fastapi import FastAPI

import sentry_sdk
from app.services import telegram_service

SENTRY_DSN = ""

# https://docs.sentry.io/platforms/python/guides/fastapi/
sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    # database.on_start_up()
    await telegram_service.startup()
    pass


@app.on_event("shutdown")
async def on_shutdown():
    await telegram_service.shutdown()
    # database.on_shutdown()
    pass
