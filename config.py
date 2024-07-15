from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY :str
    ALGORITHM :str
    ACCESS_TOKEN_EXPIRE_MINUTES :int

    class Config:
        env_file = ".env"

settings = Settings()

#its not getting print in same folder but when we impoer it is working idont know why
