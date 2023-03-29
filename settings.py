from pydantic import BaseSettings


class EnvBinance(BaseSettings):
    API_KEY: str
    SECRET: str
    BASE_API_URL: str

    class Config:
        env_file = ".env_binance_spot_test"


BINANCE_SETTINGS = EnvBinance()
