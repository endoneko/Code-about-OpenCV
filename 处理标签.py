import os


def replace_car_with_zero(directory):
    # 遍历指定目录及其子目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):  # 确保是txt文件
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 替换car为0
                content = content.replace('dewdrop', '5')

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'文件 {file_path} 已更新。')


# 使用示例
# 将'your_directory_path'替换为你的文件夹路径
replace_car_with_zero(r'F:\YOLOdata\newpic-1')