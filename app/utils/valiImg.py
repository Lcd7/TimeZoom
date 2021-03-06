import random
import string
# Image:一个画布
# ImageDraw:一个画笔
# ImageFont:画笔的字体

# pip install pillow
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

class Captcha(object):
    # 生成几位数的验证码
    number = 4
    size = (100, 30)
    fontsize = 25
    #加入干扰线条数
    lineNumber = 3

    #构建一个验证码源文本
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    #用来绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill = cls.__gene_random_color(), width = 2)

    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls, draw, pointChance, width, height):
        chance = min(100, max(0, int(pointChance))) #大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill = cls.__gene_random_color())

    # 生成随机的颜色
    @classmethod
    def __gene_random_color(cls, start = 0, end = 255):
        random.seed()
        return (random.randint(start, end),random.randint(start, end), random.randint(start, end))

    # 选择字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'Verdana.ttf',
            'verdanab.ttf',
            'verdanai.ttf',
            'verdanaz.ttf'
        ]
        font = random.choice(fonts)
        return './app/utils/font/' + font

    # 用来随机生成一个字符串
    @classmethod
    def gene_text(cls, number):
        #num是生成验证码的位数
        return ''.join(random.sample(cls.SOURCE, number))

    # 生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        width, height = cls.size
        #创建图片
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        #验证码的字体
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        draw = ImageDraw.Draw(image)
        text = cls.gene_text(cls.number)
        fontWidth, fontHeight = font.getsize(text)
        #画画
        draw.text(((width - fontWidth) / 2, (height - fontHeight) / 2), text, font = font,
                  fill = cls.__gene_random_color(150, 255))
        #干扰线
        for _ in range(0, cls.lineNumber):
            cls.__gene_line(draw, width, height)
        #绘制噪点
        cls.__gene_points(draw, 20, width, height)

        #将图片保存到内存中
        f = BytesIO()
        image.save(f, 'png')
        #从内存中取出bytes类型的图片
        data = f.getvalue()
        #将bytes转成base64
        data = base64.b64encode(data).decode()

        return (text, data)

if __name__ == "__main__":
    text, image = Captcha.gene_graph_captcha()
    # print(type(image))
    print(text)

    from io import BytesIO
    import base64
    #将图片保存到内存中
    f = BytesIO()
    image.save(f, 'png')
    #从内存中取出bytes类型的图片
    data = f.getvalue()
    #将bytes转成base64
    data = base64.b64encode(data).decode()
    print(data)

    # image.save('./app/utils/font/image.png')
