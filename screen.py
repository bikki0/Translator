import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Screen:
    # raspberry Pi pin configuration
    RST = 24
    # note the following are only used with SPI
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self, color=255):
        # setup screen
        self.color = color
        self._display = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST)
        self._display.begin()
        self._display.clear()
        self._display.display()
        self.width = self._display.width
        self.height = self._display.height

    def display_text(self, text):
        # create blank image for drawing
        image = Image.new('1', (self.width, self.height))

        # get drawing object to draw on image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('8bit.ttf', 20)
        text_width, text_height = draw.textsize(text, font=font)
        draw.text(((self.width - text_width) / 2, (self.height - text_height) / 2), text, font=font, fill=self.color)

        # display rendered image
        self._display.image(image)
        self._display.display()
