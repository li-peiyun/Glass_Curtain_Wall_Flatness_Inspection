"""
该脚本用于裁剪掉图像中可能存在的绿色窗框部分，方便计算反射边缘坐标。
"""

import cv2
import numpy as np


def crop_green_edges(image):
    """
    该函数用于裁剪掉分割图像中可能存在的绿色窗框部分。

    参数:
    - image: 分割后的图像。

    返回值:
    - cropped_image: 裁剪掉绿色窗框的图像。
    """

    # 将图像转换为HSV色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义绿色范围
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # 创建掩码
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # 找到绿色边缘的坐标
    top_edge = 0
    bottom_edge = image.shape[0]
    left_edge = 0
    right_edge = image.shape[1]

    # 上边缘
    for i in range(int(0.1 * image.shape[0])):
        if np.any(mask[i]):
            top_edge = i

    # 下边缘
    for i in range(image.shape[0]-1, int(0.9 * image.shape[0]), -1):
        if np.any(mask[i]):
            bottom_edge = i

    # 左边缘
    for i in range(int(0.08 * image.shape[1])):
        if np.any(mask[:, i]):
            left_edge = i

    # 右边缘
    for i in range(image.shape[1]-1, int(0.92 * image.shape[1]), -1):
        if np.any(mask[:, i]):
            right_edge = i

    # 偏移
    offset = 14
    # 裁剪图像
    cropped_image = image[top_edge + offset:bottom_edge - offset, left_edge + offset:right_edge - offset]

    return cropped_image


# 测试
if __name__ == "__main__":
    image_path = 'split/s2.png'
    image = cv2.imread(image_path)

    cropped_image = crop_green_edges(image)

    cv2.namedWindow('cropped image', cv2.WINDOW_NORMAL)
    cv2.imshow("cropped image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
