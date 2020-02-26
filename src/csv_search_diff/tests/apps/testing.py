from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from . import test_settings
import time
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import inspect
import logging
import math


class CsvSettingsStaticLiverServerTestCase(StaticLiveServerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csvInputDir = test_settings.CSV_DIR


class ScreenShotManager:
    __ymd: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fmt: str = '%Y%m%d'
        self.__ymd = time.strftime(fmt, time.localtime())
        # logger = logging.getLogger(__name__)
        try:
            frame = self.__get_caller_frame_info(1)
            # logger.debug(f"frame = {frame}")
            module_name = self.__get_caller_module_name(frame)
        finally:
            del frame
        self.screenshot_dir = test_settings.SCREEN_SHOT_DIR.joinpath(self.__ymd).joinpath(module_name)
        if not self.screenshot_dir.exists():
            self.screenshot_dir.mkdir(parents=True)

    def clear_screenshot_of_class(self, class_frame_depth: int = 1):
        glob_format: str = '{0:s}_*_[0-9][0-9].jpg'
        try:
            call_frame = self.__get_caller_frame_info(class_frame_depth)
            class_name = self.__get_caller_class_name(call_frame)
        finally:
            del call_frame
        path_list = Path.glob(self.screenshot_dir, glob_format.format(class_name))
        for path in path_list:
            if path.is_file():
                path.unlink()

    def save_screenshot(self, web_driver: WebDriver, element: WebElement = None, call_frame_depth: int = 1):
        if element is None:
            self.save_screenshot_for_fullsize(web_driver, call_frame_depth=call_frame_depth+1)
        else:
            self.save_screenshot_for_element(element, call_frame_depth=call_frame_depth+1)

    def save_screenshot_for_element(self, web_element: WebElement, call_frame_depth: int):
        screenshot_path = self.__get_screenshot_filepath(call_frame_depth)
        web_element.screenshot(screenshot_path)

    def save_screenshot_for_fullsize(self, web_driver: WebDriver, call_frame_depth: int = 1):
        screen_shot_path = self.__get_screenshot_filepath(call_frame_depth)
        main_element = web_driver.find_element_by_tag_name('html')
        main_element.screenshot(screen_shot_path)

    def __get_screenshot_filepath(self, call_frame_depth: int) -> str:
        fmt: str = '{0:s}_{1:s}_{2:0>2d}.jpg'
        glob_pattern: str = '{0:s}_{1:s}_[0-9][0-9].jpg'

        try:
            caller_frame = self.__get_caller_frame_info(call_frame_depth + 1)
            caller_class_name = self.__get_caller_class_name(caller_frame)
            caller_function_name = self.__get_caller_function_name(caller_frame)
        finally:
            del caller_frame

        files = self.screenshot_dir.glob(glob_pattern.format(caller_class_name, caller_function_name))
        index_num = len(list(files)) + 1

        screen_shot_path = str(
            self.screenshot_dir.joinpath(
                fmt.format(caller_class_name, caller_function_name, index_num)))
        return screen_shot_path

    def __get_caller_frame_info(self, depth: int = 0):
        frame_records = inspect.stack()
        real_depth = depth + 1
        return frame_records[real_depth]

    def __get_caller_class_name(self, frame_info: inspect.FrameInfo):
        arginfo = inspect.getargvalues(frame_info.frame)

        return arginfo.locals['self'].__class__.__name__ if 'self' in arginfo.locals else arginfo.locals['cls'].__name__

    def __get_caller_function_name(self, frame_info: inspect.FrameInfo):
        return frame_info.function

    def __get_caller_module_name(self, frame_info: inspect.FrameInfo):
        return Path(frame_info.filename).stem


