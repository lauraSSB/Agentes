from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_FINANCE_AGENT_DIR = Path(__file__).resolve().parent


class FinanceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_FINANCE_AGENT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    whatsapp_verify_token: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str


settings = FinanceSettings()