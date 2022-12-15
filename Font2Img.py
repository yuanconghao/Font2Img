# coding=utf-8
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import time

font_dir = r'./fonts/'
save_dir = r'./data/'
words_dir = r'dict/words1.txt'  # 常用汉字，目前已收录3877汉字
img_size_w = 128
img_size_h = 128


def build_dict():
    """ 打开字典，加载全部字符到list
        每行是一个字
    """
    with open(words_dir) as f:
        content = f.read()
    dict = content.split(' ')
    return dict


def draw_txt(n, charset, size):
    # 初始字体大小
    img_w, img_h = (size[0], size[1])
    factor = 1

    font_files = os.listdir(font_dir)
    for font_file in font_files:
        # 子目录跳过
        if os.path.isdir(font_file):
            continue
        # 非字体跳过
        font_file_arr = os.path.splitext(font_file)
        if font_file_arr[1] not in ['.ttf', '.TTF']:
            continue

        print('=========={} start=========='.format(font_file_arr[0]))
        start_time = time.time()

        font_file = os.path.join(font_dir, font_file)

        # 遍历所有字
        for i in range(n):
            char = charset[i]  # 当前字
            # 遍历字体
            # 数据增强
            # 创建画布
            canvas = np.zeros(shape=(img_w, img_h), dtype=np.uint8)
            canvas[0:] = 255
            # 从ndarray转成image进行渲染
            ndimg = Image.fromarray(canvas).convert('RGBA')
            draw = ImageDraw.Draw(ndimg)

            font = ImageFont.truetype(font_file, int(img_h * factor), 0)
            # 获取当前字体下的文本区域大小
            text_size = font.getsize(char)

            # 自动调整字体大小避免超出边界, 至少留白水平10%
            margin = [img_w - int(0.2 * img_w), img_h - int(0.2 * img_h)]
            while (text_size[0] > margin[0]) or (text_size[1] > margin[1]):
                factor -= 0.01  # 控制字体大小
                font = ImageFont.truetype(font_file, int(img_h * factor), 0)  # 加载字体
                text_size = font.getsize(char)

            # 随机平移
            horizontal_space = int(img_w - text_size[0]) / 2
            vertical_space = int(img_h - text_size[1]) / 2
            # 绘制当前文本行
            draw.text((horizontal_space, vertical_space), char, font=font, fill=(0, 0, 0, 255))
            img_array = np.array(ndimg)
            # 转灰度图
            img = img_array[:, :, 0]  # [32, 256, 4]
            # 生成保存路径
            img = Image.fromarray(img)
            save_dir_font = "{}/{}/".format(save_dir, font_file_arr[0])
            if not os.path.exists(save_dir_font):
                os.makedirs(save_dir_font)
            img.save(save_dir_font + '%s' % char + '.png')

        end_time = time.time()
        print('=========={} finish=========='.format(font_file_arr[0]))
        print('==========waste:{}=========='.format(end_time - start_time))


if __name__ == '__main__':
    # 图像尺寸
    size = (img_size_w, img_size_h)  # w, h
    # 字体list，每一个字符遍历所有字体，依次输出
    charset = build_dict()
    n = len(charset)
    # 字符集，将其中的字符保存成图像
    draw_txt(n, charset, size)
    print('all finish')
