from blacksheep import Application, get, json, post
from rodi import Container

from clarity.settings import SettingsLoader


class ClarityDashboardAPI(Application):
    services: Container

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.services.add_singleton(SettingsLoader)


app = ClarityDashboardAPI()
app.use_cors(
    allow_methods="*",
    allow_origins="*",
)


@get('/api')
async def home():
    return 'API Works.'


@get('/api/settings')
async def get_settings(loader: SettingsLoader):
    if loader.settings:
        return json(loader.settings.model_dump())
    elif loader.settings_error:
        return json(loader.settings_error.errors(), status=400)
    raise RuntimeError('Unknown error!')


@post('/api/settings')
async def reload_settings(loader: SettingsLoader):
    loader.load()

    if loader.settings:
        return json(loader.settings.model_dump())
    elif loader.settings_error:
        return json(loader.settings_error.errors(), status=400)
    raise RuntimeError('Unknown error!')
