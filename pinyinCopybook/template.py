from PIL import Image, ImageFont, ImageDraw


class Template:

    def __init__(self):
        self._gen_map = {
            "A4": self.generate_a4_page,
        }

    def __call__(self, name="A4"):
        assert name in self._gen_map, f"{name} template is note available"

        return self._gen_map[name]()

    @classmethod
    def generate_a4_page(cls):
        image = Image.new("RGB", size=(595,842), color='white')
        return image