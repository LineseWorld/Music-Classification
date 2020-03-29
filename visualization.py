import matplotlib.pyplot as plt
import random
import pygal,jieba
from imageio import imread
from wordcloud import  WordCloud
import PIL.Image as image
# 中文文字编码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# matplotlib 折线图 demo
# def draw_line_demo():
#     """
#     折线图
#     :return:
#     """
#     x = [1,2,3,4,5]
#     y = [1,4,9,16,25]
#     plt.plot(x,y,linewidth=3)
#     # 设置标题 给坐标轴添标签
#     plt.title("折线图",fontsize=14)
#     plt.xlabel("value",fontsize=14)
#     plt.ylabel("function",fontsize=14)
#
#     #设置刻度标记大小
#     plt.tick_params(axis='both',labelsize = 14)
#     plt.show()

# matplotlib 散点图 demo
# def draw_dots_demo():
#     """
#     散点图
#     :return:
#     """
#     # 设置标题 给坐标轴添标签
#     plt.title("折线图", fontsize=14)
#     plt.xlabel("value", fontsize=14)
#     plt.ylabel("function", fontsize=14)
#     # 设置刻度标记大小
#     plt.tick_params(axis='both', labelsize=14)
#     # x= [1,2,3,4,5]
#     # y= [1,4,9,16,25]
#     x = list(range(1,1001))
#     y = [i**2 for i in x]
#     # edgecolors 删除点轮廓颜色 c = RGB颜色
#     plt.scatter(x,y,edgecolors='none',c='blue',s=10) # s为点的大小
#     # 设置坐标轴取值范围
#     plt.axis([0,1100,0,1100000])
#     # plt.show()
#     plt.savefig('demo.png')


# pygal 折线图 demo
def pygal_line():
    """
    pygal 折线绘制
    :return:
    """
    line_chart = pygal.Line()
    line_chart.title = '折线图'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.render_to_file("line-basic.svg")


# pygal 柱形图 demo
def pygal_bar():
    bar_chart = pygal.Bar(print_values=True,print_values_position='top')  # Then create a bar graph object
    bar_chart.x_labels = map(str, range(15))
    bar_chart.title = "柱状图"
    bar_chart.add('斐波那契', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    bar_chart.render_to_file('bar_chart.svg')  # Save the svg to a file


# pygal 圆饼图 demo
def pyga_pie():
    pie_chart = pygal.Pie(inner_radius=.4)
    pie_chart.title = '饼状图'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie_chart.render_to_file("pie_chat.svg")

# 描绘词云并保存
def draw_cloud(file_name,save_name,bg_name):
    """
    生成词云
    :param file_name: 词汇文件名
    :param save_name: 存储词云图名
    :param bg_name: 背景图片
    :return:
    """
    with open(file_name,encoding='utf-8') as fp:
        text = fp.read()
        # 结巴分词
        cut_text = " ".join(jieba.cut(text))
        color_mask = imread(bg_name)
        cloud = WordCloud(
            # 设置字体，不指定就会出现乱码
            font_path="source\msyh.ttc",
            # font_path=path.join(d,'simsun.ttc'),
            # 设置背景色
            background_color='white',
            # 词云形状
            mask=color_mask,
            # 大小
            width=500,
            height=400,

            # 允许最大词汇
            max_words=2000,
            # 最大号字体
            max_font_size=100
        )
        wc = cloud.generate(cut_text)
        wc.to_file(save_name)  # 保存图片
        # 显示词云
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    # pygal_line()
    # pygal_bar()
    # pie_demo()
    file_name="source/ciyun.txt"
    save_name="user_pic/user_cloud.jpg"
    bg_name="source/bg2.png"
    draw_cloud(file_name,save_name,bg_name)