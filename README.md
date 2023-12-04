# pinyinCopybook

拼音汉字田字格A4模版, 排版后生成Pillow Image, 不依赖外部排版包

==================================

## 使用说明

目前支持A4纸，每行8格、12格汉字拼音混排，以及纯拼音版式。如有其他格式需求，可以自行扩展。

* 每页8行，每行8格拼音混排，使用:

``` python
from pinyinCopybook import Template

page = Template.generate_a4_grid_page(8)
```

* 每页11行，每行12格拼音混排，使用:

``` python
page = Template.generate_a4_grid_page(12)
```

* 纯拼音，使用:

``` python
page = Template.generate_a4_pinyin_page()
```

* 添加汉字和对应拼音

``` python
page.add_content('你', 'nǐ')
page.add_content('好', 'hǎo')
page.add_content('，', '，', 0, 1)
page.add_content('拼', 'pīn')
page.add_content('音', 'yīn')
page.add_content('世', 'shì')
page.add_content('界', 'jiè')
success = page.add_content('！', '！', 0, 1)
```

<img alt="hello, pinyin world" src="doc/hello.png" />

自动换行，当写满一页时返回 ```False```；更详细的用法请参考tests中的例子。

## 开源协议

本软件采用Apache 2.0协议，使用时请保留原始许可声明。

## 捐赠方式

如果您愿意给予我一点小小的支持，请扫码捐赠一杯咖啡吧，非常感谢！

| 支付宝 | 微信支付 |
| :------: | :------: |
| <img width="200" height="200" src="doc/zfb_pay.jpg" /> | <img width="200" height="200" src="doc/wechat_pay.jpg" /> |

## 页面效果

* 每行8格拼音混排，适用阅读入门阶段

    <img alt="每行8格" src="tests/a4_big.png" />

* 每行12格拼音混排，适用开始段落阅读阶段

    <img alt="每行12格" src="tests/a4.png" />

* 纯拼音版式，适合强化整体音节拼读

    <img alt="纯拼音" src="tests/a4_pinyin.png" />