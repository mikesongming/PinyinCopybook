import pytest
from pathlib import Path

from pinyinCopybook import Template


@pytest.fixture
def page_with_outline():
    page = Template.generate_a4_grid_page(12)
    return page

@pytest.fixture
def sample_content():
    hanzis = list('爱德华熊下楼来了')+['，“']+ list('梆、梆、梆') + ['”，'] + list('他被克里斯托弗·罗宾倒着拖在身后，脑袋一下下撞着台阶。他一直相信楼梯就是这么下的，虽然有时自己也会觉得，可能还有更好的方式吧') + ['······'] + list('如果他的头少被磕一磕，能动脑子想想就好了。不过后来他还是确定，这应该就是唯一的下法。现在，他就站在楼梯脚下，正等着认识你。他叫维尼阿噗。')
    pinyins = 'ài dé huá xióng xià lóu lái le ，“ bāng 、 bāng 、 bāng ”， tā bèi kè lǐ sī tuō fú · luó bīn dào zhe tuō zài shēn hòu ， nǎo dài yī xià xià zhuàng zhe tái jiē 。 tā yì zhí xiāng xìn lóu tī jiù shì zhè me xià de ， suī rán yǒu shí zì jǐ yě huì jué de ， kě néng hái yǒu gèng hǎo de fāng shì ba ······ rú guǒ tā de tóu shǎo bèi kē yī kē ， néng dòng nǎo zi xiǎng xiǎng jiù hǎo le 。 bù guò hòu lái tā hái shì què dìng ， zhè yīng gāi jiù shì wéi yī de xià fǎ 。 xiàn zài ， tā jiù zhàn zài lóu tī jiǎo xià ， zhèng děng zhe rèn shí nǐ 。 tā jiào wéi ní ā pū 。'.split()
    is_hanzis = [1]* len(pinyins)
    is_hanzis[8] = is_hanzis[10] = is_hanzis[12] = is_hanzis[14] = is_hanzis[22] = is_hanzis[31] = is_hanzis[41] = is_hanzis[55] = is_hanzis[66] = is_hanzis[77] = is_hanzis[88] = is_hanzis[98] = is_hanzis[108] = is_hanzis[119] = is_hanzis[122] = is_hanzis[131] = is_hanzis[138] = is_hanzis[145] = 0
    is_punctuations = [0] * len(pinyins)
    is_punctuations[8] = is_punctuations[10] = is_punctuations[12] = is_punctuations[14] = is_punctuations[22] = is_punctuations[31] = is_punctuations[41] = is_punctuations[55] = is_punctuations[66] = is_punctuations[77] = is_punctuations[88] = is_punctuations[98] = is_punctuations[108] = is_punctuations[119] = is_punctuations[122] = is_punctuations[131] = is_punctuations[138] = is_punctuations[145] = 1
    return hanzis, pinyins, is_hanzis, is_punctuations

def test_a4_grid(page_with_outline, sample_content):
    page = page_with_outline
    page.add_title('小熊维尼', '姓名:      班级:      ')

    for _ in range(1):
        for h,p,ih,ip in zip(*sample_content):
            if not page.add_content(h, p, ih, ip):
                break

    page.show()
    page.export_to_png("tests/a4.png")
    assert Path("tests/a4.png").exists()