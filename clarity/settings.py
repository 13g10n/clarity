from typing import Any

from pydantic.fields import FieldInfo, Field, computed_field
from pydantic_core import Url
from yaml import safe_load

from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class YAMLSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        raise NotImplemented

    def __call__(self) -> dict[str, Any]:
        with open('/clarity/clarity.yaml') as file:
            data = safe_load(file)

        return data


class Header(BaseModel):
    title: str = 'Welcome'
    date_format: str = 'EEEE, d MMMM yyyy'


class Application(BaseModel):
    title: str = Field(max_length=128)
    subtitle: str | None = Field(None, max_length=128)
    url: Url = Field(exclude=True)
    icon: str | None = None

    @computed_field
    def host(self) -> str:
        return self.url.host.lower()

    @computed_field
    def href(self) -> str:
        return str(self.url)


class Settings(BaseSettings):
    header: Header
    apps: list[Application] = []

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, YAMLSettingsSource(settings_cls)


class SettingsLoader:
    settings: Settings | None
    settings_error: ValidationError | None

    def __init__(self):
        self.load()

    def load(self):
        self.settings = None
        self.settings_error = None

        try:
            self.settings = Settings()
        except ValidationError as error:
            self.settings_error = error
