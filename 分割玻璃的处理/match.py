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
    cropped_images, cropped_positions, adjacency_dict = split_glass_wall(image)

    # 各玻璃的位置信息
    positions = []

    # 存储每个分割后图像的反射图像边缘坐标范围信息
    all_edges = {}

    for idx, img in enumerate(cropped_images):
        # 切除绿色边框
        cropped_img, relative_position = crop_green_edges(img)

        # 计算位置信息
        x, y = cropped_positions[idx]
        relative_x, relative_y = relative_position
        positions.append((x + relative_x, y + relative_y))

        # 获取反射图像边缘信息
        edges, _ = detect_reflected_edges(cropped_img)

        # 存储edges信息
        all_edges[idx] = edges

    # 打印位置信息（测试）
    print("所有玻璃位置信息（左上角坐标）：", positions)

    # 允许的误差范围
    tolerance = 4

    # 比较相邻图像的反射图像边缘坐标范围是否一致
    for idx in range(len(adjacency_dict)):
        # 得到该图像的邻接关系
        adjacents = adjacency_dict[idx]

        # 检查上侧是否有邻接
        # 现在只有上侧邻接的判断情况，如果测试通过补充左右下的判断！！！考虑写成函数？
        for adjacent in adjacents['up']:
            # 只检测坐标大于当前图像的，避免重复检测
            if adjacent > idx:
                # 打印当前窗户和上邻接窗户边缘坐标（测试）
                print("idx : ", idx)
                print("adjacent : ", adjacent)
                print(all_edges[idx])
                print(all_edges[adjacent])
                # 当前图片反射图像存在上边缘
                if len(all_edges[idx]['top']):
                    # 上邻接图片反射图像存在下边缘
                    if len(all_edges[adjacent]['bottom']):
                        # 两个邻接窗户的反射边缘相对横坐标
                        # 现在只考虑边缘只有一组范围的情况，如果测试中发现可能有多段范围，再进行修改！！！
                        cur_edge_r, cur_edge_l = all_edges[idx]['top'][0]
                        adj_edge_r, adj_edge_l = all_edges[adjacent]['bottom'][0]
                        # 两个邻接窗户的横坐标
                        cur_cropped_x, _ = positions[idx]
                        adj_cropped_x, _ = positions[adjacent]
                        # 两个邻接窗户的反射边缘绝对横坐标
                        cur_r = cur_edge_r + cur_cropped_x
                        cur_l = cur_edge_l + cur_cropped_x
                        adj_r = adj_edge_r + adj_cropped_x
                        adj_l = adj_edge_l + adj_cropped_x
                        # 比较横坐标范围是否一致
                        if abs(cur_r - adj_r) < tolerance and abs(cur_l - adj_l) < tolerance:
                            print("true")
                        else:
                            print("false")
                    # 上邻接图片反射图像不存在下边缘
                    else:
                        cur_edge_r, cur_edge_l = all_edges[idx]['top'][0]
                        # 如果当前窗户上边缘坐标范围小于误差允许
                        if abs(cur_edge_r - cur_edge_l) < tolerance:
                            print("true")
                        else:
                            print("false")
                # 当前图片反射图像不存在上边缘
                else:
                    # 上邻接图片反射图像存在下边缘
                    if len(all_edges[adjacent]['bottom']):
                        adj_edge_r, adj_edge_l = all_edges[adjacent]['bottom'][0]
                        # 如果上邻接窗户下边缘坐标范围小于误差允许
                        if abs(adj_edge_r - adj_edge_l) < tolerance:
                            print("true")
                        else:
                            print("false")
                    # 上邻接图片反射图像不存在下边缘
                    else:
                        print("true")


if __name__ == "__main__":
    file_path = "data/split.png"
    image = cv2.imread(file_path)
    match_reflected_edges(image)
