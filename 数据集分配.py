import os
import shutil
import random

# 指定源文件夹路径
source_images_folder = r'F:\YOLOdata\Pests_diseases\Image'
source_labels_folder = r'F:\YOLOdata\Pests_diseases\Annotation'

# 指定目标文件夹路径
target_train_images_folder = r'F:\YOLOdata\pets\images\train'
target_train_labels_folder = r'F:\YOLOdata\pets\labels\train'
target_test_images_folder = r'F:\YOLOdata\pets\images\test'
target_test_labels_folder = r'F:\YOLOdata\pets\labels\test'
target_val_images_folder = r'F:\YOLOdata\pets\images\val'
target_val_labels_folder = r'F:\YOLOdata\pets\labels\val'

# 确保目标文件夹存在，如果不存在则创建
for folder in [target_train_images_folder, target_train_labels_folder,
               target_test_images_folder, target_test_labels_folder,
               target_val_images_folder, target_val_labels_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 获取所有图像文件名（不包括扩展名）
image_file_names = set(os.path.splitext(file)[0] for file in os.listdir(source_images_folder))

# 获取所有标签文件名（不包括扩展名）
label_file_names = set(os.path.splitext(file)[0] for file in os.listdir(source_labels_folder))

# 确保文件名匹配
common_file_names = list(image_file_names.intersection(label_file_names))

# 打乱文件名列表以随机分配数据集
random.shuffle(common_file_names)

# 定义数据集比例
train_ratio = 0.8
test_ratio = 0.0
val_ratio = 0.2

# 计算训练集、测试集、验证集的文件数量
total_files = len(common_file_names)
train_files = int(total_files * train_ratio)
test_files = int(total_files * test_ratio)
val_files = total_files - train_files - test_files

# 分配文件到不同的数据集
for i, file_name in enumerate(common_file_names):
    # 复制图片文件
    if i < train_files:
        target_images_folder = target_train_images_folder
        target_labels_folder = target_train_labels_folder
    elif i < train_files + test_files:
        target_images_folder = target_test_images_folder
        target_labels_folder = target_test_labels_folder
    else:
        target_images_folder = target_val_images_folder
        target_labels_folder = target_val_labels_folder

    # 构建完整的文件路径
    image_file_path = os.path.join(source_images_folder, file_name + '.jpg')  # 假设图像文件为jpg格式
    label_file_path = os.path.join(source_labels_folder, file_name + '.txt')  # 假设标签文件为txt格式

    # 复制文件到目标文件夹
    shutil.copy(image_file_path, target_images_folder)
    shutil.copy(label_file_path, target_labels_folder)

print("Datasets have been created with the following files:")
print(f"Training set: {train_files} files")
print(f"Testing set: {test_files} files")
print(f"Validation set: {val_files} files")