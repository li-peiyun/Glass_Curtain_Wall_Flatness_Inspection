"""
      额外的分割方法尝试
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_grid(image_path, area_threshold):
    image = cv2.imread(image_path)
    # 转化为灰度图片
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=10)

    # 定义函数计算交点
    def line_intersection(line1, line2):
        x1, y1, x2, y2 = line1[0]
        x3, y3, x4, y4 = line2[0]

        # 计算两个向量的行列式
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        det1 = det([x1, y1], [x2, y2])
        det2 = det([x3, y3], [x4, y4])
        div = det([x1 - x2, y1 - y2], [x3 - x4, y3 - y4])

        # 确保除数不为零
        if div == 0:
            return np.inf, np.inf  # 不相交或平行线

        d = (det1, det2)
        x = det(d, [x1 - x2, x3 - x4]) / div
        y = det(d, [y1 - y2, y3 - y4]) / div
        return x, y

    # 计算所有交点
    intersections = []
    for i, line1 in enumerate(lines):
        for line2 in lines[i + 1:]:
            p = line_intersection(line1, line2)
            if 0 <= p[0] < gray.shape[1] and 0 <= p[1] < gray.shape[0]:  # 确保交点在图像内
                intersections.append(p)

    # 转换为numpy数组方便计算
    intersections = np.array(intersections)

    # 使用面积阈值过滤交点
    if len(intersections) == 0:
        print("No intersections were detected.")
        return

    # 计算所有点的成对距离
    dist_matrix = np.sqrt(np.sum((intersections[:, np.newaxis] - intersections[np.newaxis, :]) ** 2, axis=2))
    # 筛选距离在一定阈值内的点作为有效交点
    valid_intersections = intersections[np.all(dist_matrix > area_threshold, axis=1)]

    # 绘制直线
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 绘制交点
    for p in valid_intersections:
        cv2.circle(image, (int(p[0]), int(p[1])), 5, (0, 255, 0), -1)

    # 使用matplotlib显示图像
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Detected Grid with Area Threshold')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    file_path = "data/split.png"
    detect_grid(file_path, area_threshold=50)





