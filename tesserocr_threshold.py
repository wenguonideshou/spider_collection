import tesserocr
from PIL import Image

image = Image.open('code2.jpg')

# 灰度处理
image = image.convert('L')
# 设置阈值，进行二值化处理
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
image.show()

result = tesserocr.image_to_text(image)
print(result)