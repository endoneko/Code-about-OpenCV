import os
import shutil

# 指定你的图片文件夹路径
source_folder_path = r'C:\Users\Endoneko\Desktop\datasets\处理完的蓝屏'
# 指定新文件夹的路径
destination_folder_path = '重命名蓝屏'

# 确保目标文件夹存在，如果不存在则创建
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

# 获取文件夹中所有文件
files = os.listdir(source_folder_path)

# 初始化计数器
counter = 1

# 遍历文件夹中的文件
for file in files:
    # 构建完整的文件路径
    file_path = os.path.join(source_folder_path, file)

    # 检查文件是否是图片（这里以.jpg, .png为例，你可以根据需要添加更多格式）
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        # 构建新的文件名，格式化为4位数，不足前面补0
        new_filename = f"{counter:04d}{os.path.splitext(file)[1]}"
        new_file_path = os.path.join(destination_folder_path, new_filename)

        # 检查新文件名是否已存在
        if not os.path.exists(new_file_path):
            try:
                # 复制并重命名文件
                shutil.copy(file_path, new_file_path)
                print(f"复制和重命名 '{file}' 到 '{new_filename}'")
            except OSError as e:
                print(f"错误的复制和重命名 '{file}' 到 '{new_filename}': {e}")
        else:
            print(f"文件 '{new_filename}' 已存在. 跳过.")

        # 增加计数器
        counter += 1

print("所有图像已重命名.")