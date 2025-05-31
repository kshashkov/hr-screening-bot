from typing import Type, Tuple, Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, YamlConfigSettingsSource


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    HR_IDS: list[int]
    DATABASE_URL: Optional[SecretStr]
    OPENAI_API_KEY: SecretStr

    class Config:
        env_file = ".env"  # this is for local development


class Prompt(BaseSettings):
    text: str

    class Config:
        yaml_file = "prompt.yaml"

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(settings_cls),
        )


class Context(BaseSettings):
    text: str

    class Config:
        yaml_file = "context.yaml"

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(settings_cls),
        )
