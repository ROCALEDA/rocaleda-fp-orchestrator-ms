from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    customers_ms: str
    candidates_ms: str


settings = Settings()
