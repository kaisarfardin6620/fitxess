from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Gym AI Service"
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str
    OPENAI_API_KEY: str | None = None
    ALLOWED_HOST_ORIGINS: List[Union[str, AnyHttpUrl]] = []

    @field_validator("ALLOWED_HOST_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()