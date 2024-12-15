import cv2
import os
import numpy as np

# 初始化ORB检测器
orb = cv2.ORB_create()

input_directory = 'blueberry'
output_directory = 'output_images'

# 自定义裁剪区域大小
CROP_SIZE = 1280  # 裁剪区域的宽和高（像素）
NUM_FEATURE_IMAGES = 10  # 可更改选择特征图片的数量
MAX_CROPS_PER_IMAGE = 5  # 每张图片最多裁剪次数

# 鼠标回调函数，用于获取用户选择的区域
def mouse_callback(event, x, y, flags, param):
    global top_left_pt, bottom_right_pt, drawing, img_copy, img, roi_features, rois

    if event == cv2.EVENT_LBUTTONDOWN:  # 左键按下，记录起始点
        drawing = True
        top_left_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放，记录结束点并绘制矩形
        drawing = False
        bottom_right_pt = (x, y)
        cv2.rectangle(img_copy, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
        cv2.imshow('Image', img_copy)

    elif event == cv2.EVENT_RBUTTONDOWN:  # 右键按下，确认选择并提取ROI特征
        confirm_region()

def confirm_region():
    global top_left_pt, bottom_right_pt, img, roi_features, rois
    if top_left_pt[0] < bottom_right_pt[0] and top_left_pt[1] < bottom_right_pt[1]:
        roi = img[top_left_pt[1]:bottom_right_pt[1], top_left_pt[0]:bottom_right_pt[0]]
        kp, des = orb.detectAndCompute(roi, None)
        if des is not None:
            rois.append(roi)
            roi_features.append((des, kp))
            print(f"Confirmed region with {len(kp)} features.")
        else:
            print("No features detected in selected region.")
    top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

# 初始化变量
drawing = False
top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)
roi_features = []
rois = []
num_crops = 0

# 记录每张图片的裁剪次数
crop_count = {}

# 确保输出目录存在
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 列出输入目录中的所有图像文件
image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# 随机选择指定数量的图片进行处理
selected_files = np.random.choice(image_files, NUM_FEATURE_IMAGES, replace=False)

for i, file_name in enumerate(selected_files):
    img_path = os.path.join(input_directory, file_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Failed to load image: {img_path}")
        continue

    resized_img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
    img_copy = resized_img.copy()

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)

    print(f"Please select a region in image {i + 1}/{NUM_FEATURE_IMAGES} by drawing a rectangle and then right-click to confirm.")
    cv2.imshow('Image', img_copy)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # 按ESC键退出
            break

    cv2.destroyAllWindows()

# 匹配和裁剪逻辑
def match_and_crop(target_img, roi_features, output_directory, file_name, crop_size):
    global num_crops, crop_count

    # 计算目标图片的特征
    kp2, des2 = orb.detectAndCompute(target_img, None)
    if des2 is None or len(kp2) == 0:
        print("No features detected in target image.")
        return

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 初始化当前图片的裁剪次数
    if file_name not in crop_count:
        crop_count[file_name] = 0

    for i, (des1, kp1) in enumerate(roi_features):
        matches = matcher.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # 只使用前50个最优匹配点
        good_matches = matches[:80]

        if len(good_matches) > 10:  # 至少10个匹配点
            for match in good_matches:
                if crop_count[file_name] >= MAX_CROPS_PER_IMAGE:
                    print(f"Maximum crops reached for {file_name}. Skipping further crops.")
                    return

                x, y = map(int, kp2[match.trainIdx].pt)

                # 计算裁剪区域范围
                x_start = max(x - crop_size // 2, 0)
                y_start = max(y - crop_size // 2, 0)
                x_end = min(x + crop_size // 2, target_img.shape[1])
                y_end = min(y + crop_size // 2, target_img.shape[0])

                cropped_img = target_img[y_start:y_end, x_start:x_end]

                if cropped_img.size > 0:
                    output_path = os.path.join(output_directory, f"cropped_{file_name}_{num_crops + 1}.jpg")
                    cv2.imwrite(output_path, cropped_img)
                    print(f"Cropped image saved to {output_path}")
                    num_crops += 1
                    crop_count[file_name] += 1

# 对所有图片进行裁剪
for file_name in image_files:
    img_path = os.path.join(input_directory, file_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Failed to load image: {img_path}")
        continue

    resized_img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
    match_and_crop(resized_img, roi_features, output_directory, file_name, CROP_SIZE)

print(f"Total cropped images: {num_crops}")

cv2.destroyAllWindows()
