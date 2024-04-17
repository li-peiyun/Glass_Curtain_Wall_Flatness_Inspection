import cv2
import numpy as np
import matplotlib.pyplot as plt


# 接受两个点的坐标来计算直线斜率
def calculate_slope(x1, y1, x2, y2):
    if x2 - x1 == 0:  # To avoid division by zero
        return float('inf')  # Infinite slope (vertical line)
    else:
        return (y2 - y1) / (x2 - x1)


# 读取图片
# image = cv2.imread('./try/split.png')
def linedetect_Image(image):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 应用Canny算法进行边缘检测
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 感兴趣的区域（ROI），这里设定为图片宽度最右侧的5%以内
    roi_start = int(gray.shape[1] * 0.89)  # 70% to the right of the image
    roi_edges = edges[:, roi_start:]

    # 在ROI中应用霍夫变换检测直线。使用HoughLinesP，它返回线段的两个端点
    # 阈值、最小线长和最大线间隙是检测直线时的参数
    roi_lines = cv2.HoughLinesP(roi_edges, 1, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=20)

    # 初始化一个图像来绘制边缘线
    roi_line_image = np.zeros_like(roi_edges)

    # 如果在ROI中检测到了直线段，就计算第一条检测到的直线段的斜率，并在ROI图像上绘制这条线段。
    # 如果没有检测到直线，斜率将被设置为None
    slope = None
    if roi_lines is not None and len(roi_lines) > 0:
        for line in roi_lines:
            x1, y1, x2, y2 = line[0]
            slope = calculate_slope(x1, y1, x2, y2)
            # Draw the line on the ROI image
            cv2.line(roi_line_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # We'll just take the slope of the first detected line for demonstration
            break

    # Show the ROI with the detected edges and the calculated slope
    plt.imshow(roi_line_image, cmap='gray')
    plt.title(f'slope of edge: {slope}')
    plt.show()

    # 输出图像的斜率
    print(slope)


if __name__ == "__main__":
    image = cv2.imread('./split/s1.png')
    linedetect_Image(image)