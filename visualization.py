import matplotlib.pyplot as plt

# 中文文字编码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def draw_line_demo():
    """
    折线图
    :return:
    """
    x = [1,2,3,4,5]
    y = [1,4,9,16,25]
    plt.plot(x,y,linewidth=3)
    # 设置标题 给坐标轴添标签
    plt.title("折线图",fontsize=14)
    plt.xlabel("value",fontsize=14)
    plt.ylabel("function",fontsize=14)

    #设置刻度标记大小
    plt.tick_params(axis='both',labelsize = 14)
    plt.show()


def draw_dots_demo():
    """
    散点图
    :return:
    """
    # 设置标题 给坐标轴添标签
    plt.title("折线图", fontsize=14)
    plt.xlabel("value", fontsize=14)
    plt.ylabel("function", fontsize=14)
    # 设置刻度标记大小
    plt.tick_params(axis='both', labelsize=14)
    # x= [1,2,3,4,5]
    # y= [1,4,9,16,25]
    x = list(range(1,1001))
    y = [i**2 for i in x]
    plt.scatter(x,y,s=2) # s为点的大小
    # 设置坐标轴取值范围
    plt.axis([0,1100,0,1100000])
    plt.show()

if __name__ == '__main__':
    # draw_line_demo()
    draw_dots_demo()