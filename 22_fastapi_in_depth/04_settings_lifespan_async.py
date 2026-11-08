"""Module 22 · Settings, startup/shutdown and async endpoints

SETTINGS  -> pydantic-settings reads config from environment variables (or a .env
             file), validates the types, and keeps secrets out of your code.
LIFESPAN  -> code that runs once when the app starts (open DB pools, HTTP clients)
             and once when it stops (close them).
ASYNC     -> `async def` endpoints can await other I/O (HTTP calls, async DB drivers)
             without blocking the server. Use plain `def` for blocking/sync code:
             FastAPI runs it in a thread pool for you.

Run it:  python 22_fastapi_in_depth/04_settings_lifespan_async.py
"""
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- 1. Settings: env vars -> typed, validated config -----------------------------------------
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SHOP_", env_file=".env", extra="ignore")

    app_name: str = "Shop API"
    debug: bool = False
    rates_url: str = "https://api.example.com/rates"
    api_key: SecretStr                                  # required, and hidden when printed


os.environ["SHOP_API_KEY"] = "sk-test-123"              # normally set by your shell/host/Azure
os.environ["SHOP_DEBUG"] = "true"                       # strings are converted to bool
settings = Settings()
print(settings.app_name, settings.debug, settings.api_key)     # Shop API True **********


# --- 2. A fake external service, so this demo runs offline ---------------------------------------
def fake_rates(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"EUR": 1.0, "INR": 90.2, "USD": 1.08})


# --- 3. Lifespan: create ONE shared async HTTP client at startup, close it at shutdown -----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(transport=httpx.MockTransport(fake_rates), timeout=5)
    print("startup: HTTP client ready")
    yield                                               # the app serves requests here
    await app.state.http.aclose()
    print("shutdown: HTTP client closed")


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)


@app.get("/health")
def health() -> dict:                                   # load balancers and Azure ping this
    return {"status": "ok"}


@app.get("/price/{amount}")
async def price(amount: float, currency: str, request: Request) -> dict:
    resp = await request.app.state.http.get(settings.rates_url)   # awaits I/O, server stays free
    rate = resp.json()[currency.upper()]
    return {"eur": amount, currency.upper(): round(amount * rate, 2)}


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    with TestClient(app) as c:                          # `with` runs startup and shutdown
        print(c.get("/health").json())
        print(c.get("/price/100?currency=inr").json())  # {'eur': 100.0, 'INR': 9020.0}
