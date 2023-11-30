from pathlib import Path
from PIL import ImageFont

fonts_root = Path(__file__).parent / 'fonts'

class Fonts:

    def __init__(self, size: int = 38) -> None:
        self._font_size = size

    @property
    def TYZ_KAITI(self):
        font_path = str((fonts_root / "TYZKai.ttf").absolute())
        return ImageFont.truetype(font_path, size=self._font_size)

    @property
    def PINYIN(self):
        font_path = str((fonts_root / "PinYin.ttf").absolute())
        return ImageFont.truetype(font_path, size=self._font_size)

    @property
    def FANGSONG(self):
        font_path = str((fonts_root / "simfang.ttf").absolute())
        return ImageFont.truetype(font_path, size=self._font_size)

    @property
    def KAITI(self):
        font_path = str((fonts_root / "Kaiti.ttf").absolute())
        return ImageFont.truetype(font_path, size=self._font_size)