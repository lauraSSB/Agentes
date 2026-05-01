from pydantic_settings import BaseSettings, SettingsConfigDict

class FinanceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="financeAgent/.env",
        extra="ignore"
    )
    
    whatsapp_verify_token: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str

settings = FinanceSettings()