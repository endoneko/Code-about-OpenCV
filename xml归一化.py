import os
import xml.etree.ElementTree as ET
import shutil

# 定义归一化函数
def normalize_coordinates(size, bbox):
    if size[0] == 0 or size[1] == 0:
        raise ValueError("图片尺寸不能为0")
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (bbox[0] + bbox[2] / 2) * dw
    y = (bbox[1] + bbox[3] / 2) * dh
    w = bbox[2] * dw
    h = bbox[3] * dh
    return (x, y, w, h)

# 定义YOLO格式的写入函数
def write_yolo_format(filename, image_size, objects):
    with open(filename, 'w') as f:
        for obj in objects:
            class_id, *bbox = obj
            try:
                norm_bbox = normalize_coordinates(image_size, bbox)
                f.write(f"{class_id} {norm_bbox[0]} {norm_bbox[1]} {norm_bbox[2]} {norm_bbox[3]}\n")
            except ValueError as e:
                print(f"处理文件时出错：{e}")

# 源文件夹路径
annotations_path = 'Fall/Annotations'
images_path = 'Fall/Images'

# 目标文件夹路径
target_annotations_path = 'Fall/txt'
target_images_path = 'Fall/image-1'

# 确保目标文件夹存在
os.makedirs(target_annotations_path, exist_ok=True)
os.makedirs(target_images_path, exist_ok=True)

# 遍历annotations文件夹中的所有XML文件
for xml_file in os.listdir(annotations_path):
    if xml_file.endswith('.xml'):
        # 解析XML文件
        tree = ET.parse(os.path.join(annotations_path, xml_file))
        root = tree.getroot()

        # 获取图片尺寸
        try:
            width = int(root.find('size/width').text)
            height = int(root.find('size/height').text)
            image_size = (width, height)
        except (AttributeError, ValueError) as e:
            print(f"解析XML文件{xml_file}时出错：{e}")
            continue

        # 初始化对象列表
        objects = []

        # 遍历所有对象
        for obj in root.iter('object'):
            class_id = obj.find('name').text
            bbox = (
                int(obj.find('bndbox/xmin').text),
                int(obj.find('bndbox/ymin').text),
                int(obj.find('bndbox/xmax').text) - int(obj.find('bndbox/xmin').text),
                int(obj.find('bndbox/ymax').text) - int(obj.find('bndbox/ymin').text)
            )
            objects.append((class_id, *bbox))

        # 写入YOLO格式的TXT文件
        txt_filename = os.path.splitext(xml_file)[0] + '.txt'
        write_yolo_format(os.path.join(target_annotations_path, txt_filename), image_size, objects)

        # 复制同名图片到目标文件夹
        image_filename = os.path.splitext(xml_file)[0] + '.jpg'  # 假设图片是jpg格式
        shutil.copy(os.path.join(images_path, image_filename), os.path.join(target_images_path, image_filename))

print("转换完成。")