from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from . import test_settings


class CsvSettingsStaticLiverServerTestCase(StaticLiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csvInputDir = test_settings.CSV_DIR
