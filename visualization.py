import matplotlib.pyplot as plt
import random,connect_sql
import pygal,jieba
from imageio import imread
from wordcloud import  WordCloud
import PIL.Image as image
# 中文文字编码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False



# pygal 折线图 demo
def pygal_line_playhobby(playlist,user_id,title="标题"):
    """
    pygal 折线绘制
    :return:
    """
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = map(str, range(300))
    line_chart.add('user:'+str(user_id),playlist)
    file_name = "user_data/playhobby_"+str(user_id)+".svg"
    line_chart.render_to_file(file_name)


# pygal 柱形图 demo
def pygal_bar_plays(plays,user_id,title="标题"):
    bar_chart = pygal.Bar(print_values=True,print_values_position='top')  # Then create a bar graph object
    bar_chart.x_labels = ['片段播放','完整播放']
    bar_chart.title = title
    bar_chart.add('user:'+str(user_id),plays)  # Add some values

    file_name = "user_data/plays_" + str(user_id) + ".svg"
    bar_chart.render_to_file(file_name)  # Save the svg to a file


# pygal 圆饼图 demo
def pyga_pie_plays(plays,user_id,title="标题"):
    pie_chart = pygal.Pie(inner_radius=.4)
    pie_chart.title = title
    data1 = float(plays[0] / (plays[0]+plays[1]))
    data1 = round(data1,3)
    data2 = 1-data1
    pie_chart.add('片段播放', data1)
    pie_chart.add('完整播放', data2)
    file_name = "user_data/plays_pie_" + str(user_id) + ".svg"
    pie_chart.render_to_file(file_name)

# 描绘词云并保存
def draw_cloud(file_name,save_name,bg_name="source/bg2.png"):
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
            width=800,
            height=600,

            # 允许最大词汇
            max_words=4000,
            # 最大号字体
            max_font_size=50
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
    # file_name="user_data/cloud_393361316.txt"
    # save_name="user_data/user_cloud.jpg"
    # bg_name="source/bg2.png"
    # draw_cloud(file_name,save_name,bg_name)
    # pygal_bar([150,258],1231,"cishu")
    plays = []
    for i in range(300):
        plays.append(i)
    pygal_line_playhobby(plays,123,)