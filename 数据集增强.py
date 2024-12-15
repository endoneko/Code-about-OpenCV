import os
import random
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

source_folder_path = r'C:\Users\Endoneko\Desktop\datasets\image'
# 指定新文件夹的路径
destination_folder_path = '处理好的图片'
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)
files = [file for file in os.listdir(source_folder_path) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

#👇👇👇👇👇👇👇👇👇👇👇👇
num_random_images = 40#改这里，这是要扩充的图片数量，扩充后的数量为：该数字*6，这里例子是扩展到240张
#👆👆👆👆👆👆👆👆👆👆👆👆
random_images = random.sample(files, min(num_random_images, len(files)))

# 初始化计数器
counter = 1

# 定义添加随机噪声的函数
def add_noise(image):
    noise = Image.new('RGB', image.size)
    pixels = noise.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return Image.blend(image, noise, 0.5)  # 50% noise, 50% original image

def rotate_image(image, degrees):
    return image.rotate(degrees, expand=True)

def resize_image(image, size):
    return image.resize(size, Image.ANTIALIAS)

def adjust_brightness_contrast(image, brightness, contrast):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    return image

for file in random_images:
    # 构建完整的文件路径
    file_path = os.path.join(source_folder_path, file)

    try:
        with Image.open(file_path) as img:
            blurred_img = img.filter(ImageFilter.BLUR)
            mirrored_img = ImageOps.mirror(img)
            gaussian_img = img.filter(ImageFilter.GaussianBlur(radius=2))
            noisy_img = add_noise(img)
            rotated_img = rotate_image(img, 90)
            resized_img = resize_image(img, (256, 256))
            adjusted_img = adjust_brightness_contrast(img, 1.5, 1.2)

            new_filename_mirrored = f"mirrored_{counter:04d}{os.path.splitext(file)[1]}"
            new_filename_gaussian = f"gaussian_{counter:04d}{os.path.splitext(file)[1]}"
            new_filename_noisy = f"noisy_{counter:04d}{os.path.splitext(file)[1]}"
            new_filename_rotated = f"rotated_{counter:04d}{os.path.splitext(file)[1]}"
            new_filename_resized = f"resized_{counter:04d}{os.path.splitext(file)[1]}"
            new_filename_adjusted = f"adjusted_{counter:04d}{os.path.splitext(file)[1]}"

            mirrored_img.save(os.path.join(destination_folder_path, new_filename_mirrored))
            gaussian_img.save(os.path.join(destination_folder_path, new_filename_gaussian))
            noisy_img.save(os.path.join(destination_folder_path, new_filename_noisy))
            rotated_img.save(os.path.join(destination_folder_path, new_filename_rotated))
            resized_img.save(os.path.join(destination_folder_path, new_filename_resized))
            adjusted_img.save(os.path.join(destination_folder_path, new_filename_adjusted))

            print(
                f"进程 '{file}' -  镜像翻转保存为 '{new_filename_mirrored}', 高斯滤波保存为'{new_filename_gaussian}', 随机噪声保存为 '{new_filename_noisy}', 旋转保存为 '{new_filename_rotated}', 缩放保存为 '{new_filename_resized}', 调整亮度对比度保存为 '{new_filename_adjusted}'")

        counter += 1
    except OSError as e:
        print(f"错误进程：'{file}': {e}")

print("所有图像已处理.")