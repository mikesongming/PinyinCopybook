import pytest
from pathlib import Path
from PIL import ImageDraw

from pinyinCopybook import Template, Fonts


@pytest.fixture
def page_with_outline():
    page = Template.generate_a4_grid_page(8)
    # draw = page.draw
    # draw.rectangle(((page._padding[0], page._padding[1]),(page.CONTENT_MAX_X, page.CONTENT_MAX_Y)), outline='gray')
    return page

@pytest.fixture
def sample_content():
    hanzis = list('爱德华熊下楼来了')+['，“']+ list('梆、梆、梆') + ['”，'] + list('他被克里斯托弗·罗宾倒着拖在身后，脑袋一下下撞着台阶。他一直相信楼梯就是这么下的，虽然有时自己也会觉得，可能还有更好的方式吧') + ['······'] + list('如果他的头少被磕一磕，能动脑子想想就好了。不过后来他还是确定，这应该就是唯一的下法。现在，他就站在楼梯脚下，正等着认识你。他叫维尼阿噗。')
    # hanzis = ['小', '熊', '维', '尼', '爱', '看', '火', '锅', '城', '，', '对', '吧', '？', '啊', '壮', '壮', '......', 'Trespass']
    pinyins = 'ài dé huá xióng xià lóu lái le ，“ bāng 、 bāng 、 bāng ”， tā bèi kè lǐ sī tuō fú · luó bīn dào zhe tuō zài shēn hòu ， nǎo dài yī xià xià zhuàng zhe tái jiē 。 tā yì zhí xiāng xìn lóu tī jiù shì zhè me xià de ， suī rán yǒu shí zì jǐ yě huì jué de ， kě néng hái yǒu gèng hǎo de fāng shì ba ······ rú guǒ tā de tóu shǎo bèi kē yī kē ， néng dòng nǎo zi xiǎng xiǎng jiù hǎo le 。 bù guò hòu lái tā hái shì què dìng ， zhè yīng gāi jiù shì wéi yī de xià fǎ 。 xiàn zài ， tā jiù zhàn zài lóu tī jiǎo xià ， zhèng děng zhe rèn shí nǐ 。 tā jiào wéi ní ā pū 。'.split()
    # pinyins = ['xiǎo', 'xióng', 'wéi', 'ní', 'ài', 'kàn', 'huǒ', 'guō', 'chéng', '，', 'duì', 'ba', '？', 'a','zhuàng', 'zhuàng', '......', 'Trespass']
    is_hanzis = [1]* len(pinyins)
    is_hanzis[8] = is_hanzis[10] = is_hanzis[12] = is_hanzis[14] = is_hanzis[22] = is_hanzis[31] = is_hanzis[41] = is_hanzis[55] = is_hanzis[66] = is_hanzis[77] = is_hanzis[88] = is_hanzis[98] = is_hanzis[108] = is_hanzis[119] = is_hanzis[122] = is_hanzis[131] = is_hanzis[138] = is_hanzis[145] = 0
    is_punctuations = [0] * len(pinyins)
    is_punctuations[8] = is_punctuations[10] = is_punctuations[12] = is_punctuations[14] = is_punctuations[22] = is_punctuations[31] = is_punctuations[41] = is_punctuations[55] = is_punctuations[66] = is_punctuations[77] = is_punctuations[88] = is_punctuations[98] = is_punctuations[108] = is_punctuations[119] = is_punctuations[122] = is_punctuations[131] = is_punctuations[138] = is_punctuations[145] = 1
    return hanzis, pinyins, is_hanzis, is_punctuations

def test_a4_grid(page_with_outline, sample_content):
    page = page_with_outline
    page.add_title('小熊维尼', '姓名:      班级:      ')

    page.show_grid = True
    page.show_tianzi = False
    page.show_pinyin_lines = True

    for _ in range(3):
        for h,p,ih,ip in zip(*sample_content):
            page.add_content(h, p, ih, ip)

    page.show()
    page.export_to_png("tests/a4_big.png")
    assert Path("tests/a4_big.png").exists()

def test_a4_no_grid():
    page = Template.generate_a4_grid_page(8, show_grid=False)
    assert not page.show_grid
    assert not page.show_tianzi
    page.add_content('熊', 'xióng', 1, 0)