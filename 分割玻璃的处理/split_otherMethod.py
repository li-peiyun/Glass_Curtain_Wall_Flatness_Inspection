import cv2
import numpy as np
from matplotlib import pyplot as plt


# 水平分割尝试
def crop_image_by_contour(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    return image[y:y + h, x:x + w]


# def crop_image_by_contour(image, contour, mask):
#     x, y, w, h = cv2.boundingRect(contour)
#     if w > 2 * h:  # 假设宽度大于高度两倍可能是两个矩形
#         # 扫描查找两个矩形的间隙
#         for i in range(x, x + w):
#             # 如果这一列有足够多的绿色像素，则认为找到了间隙
#             # 注意：这里使用mask[y:y+h, i]来仅检查这一列的绿色像素
#             if np.sum(mask[y:y + h, i]) > h * 255 * 0.05:  # 假设至少5%的像素是绿色的
#                 # 基于找到的间隙裁剪出两个矩形
#                 left_rect = image[y:y + h, x:i]
#                 right_rect = image[y:y + h, i:x + w]
#                 return [left_rect, right_rect]
#     # 否则，返回单个矩形
#     return [image[y:y + h, x:x + w]]


def glass_DetectAndSplit(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义HSV中绿色的范围
    lower_green = np.array([35, 100, 50])
    upper_green = np.array([85, 255, 255])

    # 创建一个掩模，只显示绿色范围内的部分
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
    # 树检索方法去查询轮廓
    # 从一个二值化图像中找出轮廓，这些轮廓是由相同颜色或强度的连续点组成的曲线
    # contours, _ = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    kernel = np.ones((4, 2), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 定义了一个函数来过滤掉面积小于指定最小值的轮廓。
    # 确保只考虑基于它们相对于图像大小的显著物体
    def filter_contours_by_area(_contours, _min_area):
        return [c for c in _contours if cv2.contourArea(c) > _min_area]

    # 用总面积大小的 n% 作为筛选，排除面积太小和噪声等
    min_area = image.shape[0] * image.shape[1] * 0.001  # 1% of the image area
    filtered_contours = filter_contours_by_area(contours, min_area)

    # 找到面积最大的轮廓并删除它
    max_contour = max(contours, key=cv2.contourArea)
    contours = [c for c in contours if c is not max_contour]

    # 使用删除后的最大面积作为新的面积标准
    max_area = cv2.contourArea(max(contours, key=cv2.contourArea))
    min_area = 0.9 * max_area  # 90% of the max contour area

    filtered_contours = filter_contours_by_area(contours, min_area)

    cropped_images = [crop_image_by_contour(image, c) for c in filtered_contours]

    # --------------------相邻性判断-------------------------------------
    # 判断box2相对于box1的方向
    def are_adjacent(box1, box2, tolerance=50):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        if abs(x1 + w1 - x2) <= tolerance:  # box1 is on the left of box2
            return 'right'
        elif abs(x2 + w2 - x1) <= tolerance:  # box1 is on the right of box2
            return 'left'
        elif abs(y1 + h1 - y2) <= tolerance:  # box1 is above box2
            return 'down'
        elif abs(y2 + h2 - y1) <= tolerance:  # box1 is below box2
            return 'up'
        return None

    # 得到相反方向
    def invert_direction(direction):
        if direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'
        elif direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        return None

    bounding_boxes = [cv2.boundingRect(c) for c in filtered_contours]

    # 利用字典存储相邻的信息及其位置关系
    adjacency_dict = {i: {'left': [], 'right': [], 'up': [], 'down': []} for i in range(len(bounding_boxes))}

    for i in range(len(bounding_boxes)):
        for j in range(i + 1, len(bounding_boxes)):
            direction = are_adjacent(bounding_boxes[i], bounding_boxes[j])
            if direction:
                adjacency_dict[i][direction].append(j)
                adjacency_dict[j][invert_direction(direction)].append(i)

    return cropped_images, adjacency_dict


if __name__ == "__main__":
    file_path = "data/split.png"
    image = cv2.imread(file_path)
    cropped_images, adjacency_dict = glass_DetectAndSplit(image)

    # 显示得到的图片
    for idx, img in enumerate(cropped_images):
        cv2.namedWindow('splited image', cv2.WINDOW_NORMAL)
        cv2.imshow("splited image", img)
        cv2.waitKey(0)

    # 打印邻接字典
    print("邻接字典判断相邻性：")
    for i, adjacents in adjacency_dict.items():
        print(f"{i}: {adjacents}")

    # 使用示例
    print("\n使用示例：")
    # 读取第1张图片，并显示它的邻接图片
    idx = 0
    adjacents = adjacency_dict[idx]
    print(f"图像 {idx} 的邻接图片索引：{adjacents}")

    # 显示第1张图片
    # cv2.namedWindow('Window Image', cv2.WINDOW_NORMAL)
    # cv2.imshow('Window Image', cropped_images[idx])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
