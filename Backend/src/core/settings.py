from pydantic_settings import BaseSettings, SettingsConfigDict #type: ignore

class Settings(BaseSettings):
    
    #  Copy to .env and fill in values (never commit .env)
    DB_CONNECTION : str

    # JWT settings
    ACCESS_TOKEN_SECRET : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    # Refresh Token
    REFRESH_TOKEN_EXPIRE_DAYS : int
    REFRESH_TOKEN_SECRET : str

    # Reset Token
    RESET_TOKEN_SECRET : str
    RESET_TOKEN_EXPIRE_MINUTES : int

    # Frontend Url 
    FRONTEND_URL : str

    # Email Settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    RESEND_API_KEY: str


    # AI Integration (use KEY=value only)
    GROQ_API_KEY: str
    GROQ_MODEL: str

    # Logging: use DEBUG to see message previews in the terminal
    LOG_LEVEL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()