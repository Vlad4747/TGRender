
from PIL import Image, ImageDraw

# Создайте новое изображение с белым фоном
image = Image.new("RGB", (700, 300), "black")
draw = ImageDraw.Draw(image)

# Определите ограничивающую рамку как последовательность из двух кортежей
bounding_box = [(250, 30), (450, 270)]

# Укажите радиус для закруглённых углов
radius = 16

# Нарисуйте закруглённый прямоугольник с параметрами по умолчанию
draw.rounded_rectangle(bounding_box,fill="red", radius=radius)

# Отобразите изображение
image.save("test.png")
print('Закруглённый прямоугольник успешно нарисован...')