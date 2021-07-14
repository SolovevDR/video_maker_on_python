import os
import cv2
from PIL import Image
'''
# Проверка текущего пути к каталогу

print(os.getcwd())

# Папка, которая содержит все изображения
# из которого должно быть сгенерировано видео

os.chdir("D:\\video\\image")
path = "D:\\video\\image"
mean_height = 0
mean_width = 0
num_of_images = len(os.listdir('.'))

#print (num_of_images)

for file in os.listdir('.'):
    im = Image.open(os.path.join(path, file))
    width, height = im.size
    mean_width += width
    mean_height += height

    # im.show () # раскомментируйте это для отображения изображения

# Нахождение средней высоты и ширины всех изображений.
# Это необходимо, потому что требуется видеокадр
# устанавливается одинаковой шириной и высотой. В противном случае
# изображения не равные этой ширине высота не получится
# встроено в видео

mean_width = int(mean_width / num_of_images)
mean_height = int(mean_height / num_of_images)

# print (mean_height)
# print (mean_width)


# Изменение размера изображений, чтобы дать
# их одинаковой ширины и высоты

for file in os.listdir('.'):

    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
        # открытие изображения с помощью PIL Image
        im = Image.open(os.path.join(path, file))
        # im.size включает в себя высоту и ширину изображения
        width, height = im.size
        print(width, height)
        # изменение размера
        imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)
        imResize.save(file, 'JPEG', quality=95)  # настройка качества
        # печать каждого измененного имени изображения
        print(im.filename.split('//')[-1], " is resized")

    # Функция создания видео


def generate_video():
    image_folder = '.'  # убедитесь, что используете вашу папку
    video_name = 'mygeneratedvideo.avi'
    os.chdir("D:\\video\\image")
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]

    # Изображения массива должны учитывать только
    # файлы изображений, игнорируя другие, если таковые имеются

    print(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    # настройка ширины рамки, высоты по ширине
    # ширина, высота первого изображения

    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    # Добавление изображений к видео по одному

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

        # Распределение памяти, взятой для создания окна

    cv2.destroyAllWindows()
    video.release()  # выпуск сгенерированного видео

# Вызов функции generate_video
generate_video()'''


video1 = cv2.VideoCapture('video.mp4')
video1_width = video1.get(cv2.CAP_PROP_FRAME_WIDTH)
print(video1_width)
video1_height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
video1_fps = int(video1.get(cv2.CAP_PROP_FPS))

video2 = cv2.VideoCapture('image_video.avi')

writer = cv2.VideoWriter('video3.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                         video1_fps, (int(video1_width), int(video1_height)))
writer.set(cv2.VIDEOWRITER_PROP_QUALITY, 100)

while True:
    ret, frame = video2.read()
    if not ret:
        break
    frame = cv2.resize(frame, (int(video1_width), int(video1_height)))
    writer.write(frame)

video1.release()
video2.release()
writer.release()