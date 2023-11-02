from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    customers_ms: str # = "customers_url"
    candidates_ms: str # = "candidates_url"


settings = Settings()
