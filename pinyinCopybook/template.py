from typing import List
import numpy as np
from PIL import Image, ImageDraw

from .font import Fonts


class Template:

    @classmethod
    def generate_a4_page(cls):
        return A4Page()

    @classmethod
    def generate_a4_grid_page(cls, grid_size: str, **kwargs):
        if grid_size == 'big':
            return PinYinTianZiGePage(**kwargs)
        elif grid_size == 'small':
            return PinYinTianZiGePage2(**kwargs)


class A4Page:

    _mode = 'RGB'
    _size = (595, 842)  # 72 dpi
    _color = 'white'
    _padding = (50,72,50,50)    # left,up,right,down

    TITLE_FONT_SIZE = 18
    TITLE_COLOR = (31,189,148)

    def __init__(self) -> None:
        self._image = Image.new(self._mode, self._size, self._color)
        self._draw = None

        self.TITLE_XY = (self._padding[0]+10, self._padding[1]-36)
        self.TITLE_LEFT_CONTENT_X = self.TITLE_XY[0]
        self.TITLE_RIGHT_CONTENT_X = self.TITLE_XY[0]+300

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    @property
    def draw(self):
        if self._draw is None:
            self._draw = ImageDraw.Draw(self._image)
        return self._draw
        # return ImageDraw.Draw(self._image)

    def show(self):
        self._image.show()

    def export_to_array(self):
        return np.array(self._image)

    def export_to_png(self, filename: str):
        self._image.save(filename)

    def add_title(self, left_content: str, right_content=None):
        self.draw.text((self.TITLE_LEFT_CONTENT_X, self.TITLE_XY[1]), left_content, font=Fonts(18).KAITI, fill=self.TITLE_COLOR) #53, 206, 141

        if right_content:
            self.draw.text((self.TITLE_RIGHT_CONTENT_X, self.TITLE_XY[1]+5), right_content, font=Fonts(14).KAITI, fill=(0,0,0))


class PinYinTianZiGePage(A4Page):
    COLS = 8
    ROWS = 8
    GRID_WIDTH = 60
    GRID_HEIGHT = 84

    GRID_PADDING = 5
    GRID_LINE_COLOR = (39,232,25)
    GRID_INNER_LINE_COLOR = (204,204,204)
    GRID_DASH_UNIT_LEN = 2
    PINYIN_FONT_SIZE=14
    PINYIN_UP_PADDING=4
    PINYIN_LINE1_DY = 5
    PINYIN_LINE2_DY = 13
    HANZI_FONT_SIZE=42
    HANZI_PADDING_X=9
    HANZI_PADDING_Y=9
    PUNCTUATION_SPACING = 5
    PUNCTUATION_FONT_SIZE = 32
    PUNCTUATION_PADDING_Y = 12

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.show_grid = kwargs.get('show_grid', True)
        self.show_tianzi = kwargs.get('show_tianzi', True)
        self.show_pinyin_lines = kwargs.get('show_pinyin_lines', True)
        if not self.show_grid:
            self.show_tianzi = False

        # 拼音和汉字分割线高度
        self.GRID_SEP_HEIGHT = self.GRID_HEIGHT - self.GRID_WIDTH
        self.CONTENT_MAX_X = self.width - self._padding[2]
        self.CONTENT_MAX_Y = self.height - self._padding[3]

        self.next_grid_xy = (self._padding[0] + self.GRID_PADDING, self._padding[1] + self.GRID_PADDING)

    # def add_contents(self, hanzis: List[str], pinyins: List[str], is_hanzis: List[bool], is_punctuations: List[bool]):
    #     for hanzi, pinyin, is_hanzi, is_punctuation in zip(hanzis, pinyins, is_hanzis, is_punctuations):
    #         self.add_content(hanzi, pinyin, is_hanzi, is_punctuation)

    def add_content(self, hanzi: str, pinyin: str, is_hanzi=True, is_punctuation=False) -> bool:
        """
        添加字符到田字格页面，如果页面还有空间

        Args:
            hanzi (str): 汉字或其他字符
            pinyin (str): 汉字对应拼音
            is_hanzi (bool, optional): 是否汉字
            is_punctuation (bool, optional): 是否标点符号

        Returns:
            bool: 如果字符成功写入页面, 返回True; 否则返回False, 例如页面已满
        """
        if is_hanzi:
            return self._draw_hanzi_pinyin(hanzi, pinyin)
        elif is_punctuation:
            return self._draw_punctuation(hanzi)
        else:
            return self._draw_others(hanzi, pinyin)

    def _draw_hanzi_pinyin(self, hanzi, pinyin) -> bool:
        grid_bbox, nnext_grid_xy = self._next_bbox(self.GRID_WIDTH, self.GRID_HEIGHT)

        if grid_bbox is None:
            return False
        else:
            # key points
            grid_start_xy, grid_end_xy = grid_bbox

            a0 = (grid_start_xy[0], grid_start_xy[1]+self.GRID_SEP_HEIGHT)
            b0 = (a0[0]+self.GRID_WIDTH, a0[1])
            a1 = (a0[0], grid_start_xy[1]+self.PINYIN_UP_PADDING+self.PINYIN_LINE1_DY)
            b1 = (grid_end_xy[0], a1[1])
            a2 = (a0[0], grid_start_xy[1]+self.PINYIN_UP_PADDING+self.PINYIN_LINE2_DY)
            b2 = (grid_end_xy[0], a2[1])
            a3 = (a0[0], int((a0[1]+grid_end_xy[1])/2))
            b3 = (grid_end_xy[0], a3[1])
            c1 = (grid_start_xy[0]+int(self.GRID_WIDTH/2), a0[1])
            d1 = (c1[0], grid_end_xy[1])

            if self.show_grid:
                self.draw.rectangle(grid_bbox, outline=self.GRID_LINE_COLOR, width=1)
                # mid_sep_line
                self.draw.line((a0,b0), fill=self.GRID_LINE_COLOR, width=1)

                # tian zi ge
                if self.show_tianzi:
                    self._draw_horizontal_dashed_line(a3, b3)
                    self._draw_vertical_dashed_line(c1, d1)

                # pinyin inner lines
                if self.show_pinyin_lines:
                    self._draw_horizontal_dashed_line(a1, b1)
                    self._draw_horizontal_dashed_line(a2, b2)
            else:   # no grid line
                if self.show_pinyin_lines:
                    self.draw.line((grid_start_xy, (grid_start_xy[0]+self.GRID_WIDTH, grid_start_xy[1])), fill=self.GRID_INNER_LINE_COLOR, width=1)
                    self.draw.line((a0,b0), fill=self.GRID_INNER_LINE_COLOR, width=1)
                    self._draw_horizontal_dashed_line(a1, b1)
                    self._draw_horizontal_dashed_line(a2, b2)

            # hanzi
            self._draw_hanzi_at(a0, hanzi)

            # pinyin
            self._draw_pinyin_at(grid_start_xy, pinyin)

            self.next_grid_xy = nnext_grid_xy
            return True

    def _draw_hanzi_at(self, xy: tuple[int], hanzi: str):
        hanzi_start_x, hanzi_start_y = xy
        # hzbox = self.draw.textbbox((hanzi_start_x, hanzi_start_y), hanzi, font=Fonts(self.HANZI_FONT_SIZE).TYZ_KAITI)
        hanzi_start_x += self.HANZI_PADDING_X
        hanzi_start_y += self.HANZI_PADDING_Y
        hanzi_start_xy = (hanzi_start_x, hanzi_start_y)
        self.draw.text(hanzi_start_xy, hanzi, font=Fonts(self.HANZI_FONT_SIZE).TYZ_KAITI, fill=(0,0,0))

    def _draw_pinyin_at(self, xy: tuple[int], pinyin: str):
        pinyin_start_x, pinyin_start_y = xy
        tlen = self.draw.textlength(pinyin, font=Fonts(self.PINYIN_FONT_SIZE).PINYIN)
        pinyin_start_x += int((self.GRID_WIDTH - tlen)/2)
        pinyin_start_y += self.PINYIN_UP_PADDING
        pinyin_start_xy = (pinyin_start_x, pinyin_start_y)
        self.draw.text(pinyin_start_xy, pinyin, font=Fonts(self.PINYIN_FONT_SIZE).PINYIN, fill=(0,0,0))

    def _draw_horizontal_dashed_line(self, pt1, pt2):
        assert pt1[1] == pt2[1]
        xs = range(pt1[0], pt2[0], self.GRID_DASH_UNIT_LEN)
        for i, x in enumerate(xs):
            if i % 2 == 0:
                self.draw.line((x, pt1[1], x+self.GRID_DASH_UNIT_LEN, pt1[1]), fill=self.GRID_INNER_LINE_COLOR, width=1)
        if x < pt2[0]:
            self.draw.line((x, pt1[1], pt2[0], pt1[1]), fill=self.GRID_INNER_LINE_COLOR, width=1)

    def _draw_vertical_dashed_line(self, pt1, pt2):
        assert pt1[0] == pt2[0]
        ys = range(pt1[1], pt2[1], self.GRID_DASH_UNIT_LEN)
        for i, y in enumerate(ys):
            if i % 2 == 0:
                self.draw.line((pt1[0], y, pt1[0], y+self.GRID_DASH_UNIT_LEN), fill=self.GRID_INNER_LINE_COLOR, width=1)
        if y < pt2[1]:
            self.draw.line((pt1[0], y, pt1[0], pt2[1]), fill=self.GRID_INNER_LINE_COLOR, width=1)

    def _draw_punctuation(self, hanzi) -> bool:
        grid_start_x, grid_start_y = self.next_grid_xy
        pinyin_start_xy = (grid_start_x + self.PUNCTUATION_SPACING, grid_start_y+self.GRID_SEP_HEIGHT + self.PUNCTUATION_PADDING_Y)
        font = Fonts(self.PUNCTUATION_FONT_SIZE).TYZ_KAITI
        tlen = self.draw.textlength(hanzi, font)
        if tlen > self.GRID_WIDTH:
            font = Fonts(self.PUNCTUATION_FONT_SIZE-4).TYZ_KAITI
            tlen = self.draw.textlength(hanzi, font)
        self.draw.text(pinyin_start_xy, hanzi,font=font, fill=(0,0,0))
        self.next_grid_xy = (grid_start_x+self.GRID_WIDTH, grid_start_y)
        return True

    def _draw_others(self, hanzi, pinyin) -> bool:
        font = Fonts(self.PUNCTUATION_FONT_SIZE).KAITI
        tlen = self.draw.textlength(hanzi, font=font)
        num_grids = int(np.ceil(tlen/self.GRID_WIDTH))

        grid_bbox, nnext_grid_xy = self._next_bbox(num_grids * self.GRID_WIDTH, self.GRID_HEIGHT)

        if grid_bbox is None:
            return False
        else:
            grid_start_xy, grid_end_xy = grid_bbox
            grid_start_x, grid_start_y = grid_start_xy
            start_xy = (grid_start_x + self.PUNCTUATION_SPACING, grid_start_y+self.GRID_SEP_HEIGHT + self.PUNCTUATION_PADDING_Y)
            self.draw.text(start_xy, hanzi,font=font,fill=(0,0,0))

            self.next_grid_xy = nnext_grid_xy
            return True

    def _next_bbox(self, delta_x, delta_y):
        next_grid_x, next_grid_y = self.next_grid_xy

        if next_grid_x + delta_x > self.CONTENT_MAX_X:
            # next row
            next_grid_x = self._padding[0] + self.GRID_PADDING
            next_grid_y += delta_y

        if next_grid_y + delta_y > self.CONTENT_MAX_Y:
            # next page
            return None, None

        grid_right_x = next_grid_x + delta_x
        grid_lower_y = next_grid_y + delta_y

        grid_bbox = ((next_grid_x, next_grid_y), (grid_right_x, grid_lower_y))
        nnext_grid_xy = (grid_right_x, next_grid_y)
        return grid_bbox, nnext_grid_xy


class PinYinTianZiGePage2(PinYinTianZiGePage):
    """
    格子更小，适合段落阅读
    """
    COLS = 12
    ROWS = 11
    GRID_WIDTH = 40
    GRID_HEIGHT = 60

    PINYIN_FONT_SIZE=14
    PINYIN_UP_PADDING=3
    PINYIN_LINE1_DY = 3
    PINYIN_LINE2_DY = 11
    HANZI_FONT_SIZE=32
    HANZI_PADDING_X=5
    HANZI_PADDING_Y=3
    PUNCTUATION_SPACING = 5
    PUNCTUATION_FONT_SIZE = 24
    PUNCTUATION_PADDING_Y = 9

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.show_grid = True
        self.show_tianzi = False
        self.show_pinyin_lines = False

    def _draw_pinyin_at(self, xy: tuple[int], pinyin: str):
        pinyin_start_x, pinyin_start_y = xy
        font=Fonts(self.PINYIN_FONT_SIZE).PINYIN

        tlen = self.draw.textlength(pinyin, font=font)
        if tlen > self.GRID_WIDTH:
            font=Fonts(self.PINYIN_FONT_SIZE-4).PINYIN
            tlen = self.draw.textlength(pinyin, font=font)

        pinyin_start_x += int((self.GRID_WIDTH - tlen)/2)
        pinyin_start_y += self.PINYIN_UP_PADDING
        pinyin_start_xy = (pinyin_start_x, pinyin_start_y)
        self.draw.text(pinyin_start_xy, pinyin, font=font, fill=(0,0,0))
