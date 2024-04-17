"""
！！！未完成！！！
该脚本用于读取玻璃幕墙图像，判断相邻玻璃反射图像边缘坐标范围是否匹配。
"""

import cv2
from split import split_glass_wall
from crop import crop_green_edges
from edge import detect_reflected_edges


def match_reflected_edges(image):
    # 获取分割后的玻璃图像并得到邻接关系字典
    cropped_images, adjacency_dict = split_glass_wall(image)

    # 存储每个分割后图像的反射图像边缘坐标范围信息
    all_edges = {}

    for idx, img in enumerate(cropped_images):
        # 切除绿色边框
        cropped_img = crop_green_edges(img)

        # 获取反射图像边缘信息
        edges, _ = detect_reflected_edges(cropped_img)

        # 存储edges信息
        all_edges[idx] = edges

    # 比较相邻图像的反射图像边缘坐标范围是否一致
    for idx in range(len(adjacency_dict)):
        # 得到该图像的邻接关系
        adjacents = adjacency_dict[idx]

        # 检查上侧是否有邻接
        for adjacent in adjacents['up']:
            # 只检测坐标大于当前图像的，避免重复检测
            if adjacent > idx:
                print(all_edges[idx])
                print(all_edges[adjacent])


if __name__ == "__main__":
    file_path = "data/split.png"
    image = cv2.imread(file_path)
    match_reflected_edges(image)
