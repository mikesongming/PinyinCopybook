import pytest
from pathlib import Path
from PIL import ImageDraw

from pinyinCopybook import Template, Fonts


@pytest.fixture
def page_with_outline():
    page = Template.generate_a4_page()
    draw = page.draw
    draw.rectangle(((page._padding[0], page._padding[1]),(page.width-page._padding[2], page.height-page._padding[3])), outline='gray')
    return page

def test_a4_template(page_with_outline):
    page = page_with_outline
    img = page.export_to_array()
    assert img.shape == (page.height, page.width, 3)

def test_a4_title(page_with_outline):
    page = page_with_outline
    page.add_title('CHAPTER 1 小熊维尼阿噗', '姓名:      班级:      ')
    # page.show()