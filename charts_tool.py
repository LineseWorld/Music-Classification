from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie,Tab
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts.components import Image
from pyecharts.options import ComponentTitleOpts
import random
# 柱状图
def draw_bar_plays(data,user_id,title="听歌方式"):
    """
    两种听歌方式
    :param plays:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_bar_plays.html"
    x = ["片段播放", "完整播放"]
    color = ["#749f83", "#d48265"]

    xlen = len(x)
    y = []
    for idx, item in enumerate(x):

        y.append(
            opts.BarItem(
                name=item,
                value=data[idx],
                itemstyle_opts=opts.ItemStyleOpts(color=color[idx]),
            )
        )
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("用户："+str(user_id), y,color=Faker.rand_color())
            .set_global_opts(title_opts=opts.TitleOpts(title=title),toolbox_opts=opts.ToolboxOpts())
            #.render(file_name)
    )
    return c

def draw_pie_recoder(data,user_id,title="用户行为占比"):
    """
    用户行为占比
    :param data:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_pie_recoder.html"

    c = (
        Pie(init_opts=opts.InitOpts(width="500px",height="300px"))
            .add(
            "",
            data,
            center=["25%", "50%"],
            )

            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}% "))
            .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="45%", orient="vertical"))

    )
    return c

def draw_bar_recoder(data,user_id,title = "用户行为统计"):
    """
    用户行为统计
    :param data:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_bar_recoder.html"
    x = ["循环播放","片段播放","查看评论","点赞评论","收藏歌曲"]
    color = ["#F79709","#749f83", "#d48265","#33CCCC","#82C182"]
    xlen = len(x)
    y = []
    for idx, item in enumerate(x):
        y.append(
            opts.BarItem(
                name=item,
                value=data[idx][1],
                itemstyle_opts=opts.ItemStyleOpts(color=color[idx]),
            )
        )
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("" , y, color=Faker.rand_color())
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             toolbox_opts=opts.ToolboxOpts()
                             )
            # .render(file_name)
    )
    return c

def draw_line_clip(data,user_id,title = "片段播放习惯"):
    """
    片段播放习惯
    :param playhobbys:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_line_clip.html"
    x_data = []
    for i in range(300):
        x_data.append(i)

    c = (
        Line()
            .add_xaxis(
            xaxis_data=x_data
            )
            .add_yaxis(
            "palycounts",
            data,
            symbol_size=0,
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=True
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=title, pos_left="center"
                ),

                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=True,
                    )
                ],
                xaxis_opts=opts.AxisOpts(
                    type_ = "category",
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=True)
                ),
                yaxis_opts=opts.AxisOpts(name="playcounts"),
                legend_opts=opts.LegendOpts(pos_left="left"),
                toolbox_opts=opts.ToolboxOpts(
                    is_show=True,
                    feature={
                        "dataZoom": {"yAxisIndex": "none"},
                        "restore": {},
                        "saveAsImage": {},
                    },
                ),
            )
            #.render(file_name)
    )
    return c

def draw_pie_like(data,user_id,title="偏爱曲风比重"):
    """
    圆饼图 偏爱歌曲比重
    :param data:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_pie_like.html"
    c = (
        Pie()
            .add(
            "",
            data,
            radius=["30%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{b}: {d}% ",
            ),
            center=["25%", "50%"],
        )
            .set_global_opts(
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="45%", orient="vertical")
                             )
            #.render(file_name)
    )
    return c

def draw_bar_like(data,user_id,title="偏爱曲风统计"):
    """
    柱状图 偏爱统计
    :param data:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_bar_like.html"
    x = ["古风", "古典", "电子", "民谣", "流行", "说唱", "摇滚"]
    color = ["#C43C3C", "#7D573E", "#E6E65D", "#69DA69", "#70D4D4", "#9B7CC7", "#A2A2A2"]
    xlen = len(x)
    y = []
    for idx, item in enumerate(x):
        y.append(
            opts.BarItem(
                name=item,
                value=data[idx][1],
                itemstyle_opts=opts.ItemStyleOpts(color=color[idx]),
            )
        )
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("", y, color=Faker.rand_color())
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             toolbox_opts=opts.ToolboxOpts()
                             )
            #.render(file_name)
    )
    return c

def draw_cloud(url,user_id,title = "用户词云"):
    image = Image()

    image.add(
        src=url,
        style_opts={"width": "800px", "height": "500px", "style": "margin-left: 200px"},
    )
    image.set_global_opts(
        title_opts=ComponentTitleOpts(title=title, subtitle="用户:"+str(user_id))
    )

    return image


def grid_recoder(data,user_id):
    bar = draw_bar_recoder(data, user_id)
    pie = draw_pie_recoder(data, user_id)
    grid = (
        Grid(init_opts=opts.InitOpts(width="1400px",height="500px"))
            .add(bar, grid_opts=opts.GridOpts(pos_left="55%"))
            .add(pie, grid_opts=opts.GridOpts(pos_right="55%"))

    )
    return grid

def grid_like(data,user_id):
    bar = draw_bar_like(data, user_id)
    pie = draw_pie_like(data, user_id)
    grid = (
        Grid(init_opts=opts.InitOpts(width="1400px",height="500px"))
            .add(bar, grid_opts=opts.GridOpts(pos_left="55%"))
            .add(pie, grid_opts=opts.GridOpts(pos_right="55%"))

    )
    return grid

def page_plays(data1,data2,user_id):
    bar = draw_bar_plays(data1, user_id)
    line = draw_line_clip(data2, user_id)
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        bar,
        line,
    )
    #page.render("page_simple_layout.html")
    return page

def user_tab(data_set,user_id,title="用户数据分析"):
    """

    :param data_set:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_data.html"
    url = "cloud_" + str(user_id) + ".jpg"
    tab = Tab()
    tab.add(grid_recoder(data_set[0],user_id), "用户行为统计")
    tab.add(grid_like(data_set[1],user_id), "用户偏爱分析")
    # tab.add(page_plays(data_set[2],data_set[3],user_id), "用户习惯")
    tab.add(draw_bar_plays(data_set[2], user_id), "用户播放方式")
    tab.add(draw_line_clip(data_set[3], user_id), "片段播放频率统计")
    tab.add(draw_cloud(url, user_id), "歌词词云")
    tab.render(file_name)



if __name__ == '__main__':
    print("-----")
    # bar_color_demo()
    # draw_bar_plays([10,130],111)
    #
    # grid_demo()
    data_set=[]
    data = [("循环播放", 3), ("片段播放", 2), ("查看评论", 1), ("点赞评论", 5), ("收藏歌曲", 3)]
    # page_recoder(data,222)
    data_set.append(data)
    data = [("古风", 3), ("古典", 2), ("电子", 1), ("民谣", 5), ("流行", 3), ("说唱", 1), ("摇滚", 1)]
    data_set.append(data)
    data_set.append([110,50])
    data1 = []
    for i in range(300):
         data1.append(i)
    data_set.append(data1)
    # page_plays([110,20],data1,33)
    url = "user_data/cloud_393361316.jpg"
    data_set.append(url)
    user_tab(data_set,393361316)

    # draw_cloud(url,333)
    # data1 = []
    # for i in range(300):
    #     data1.append(random.randint(0, 5))
    # draw_line_clip(data1,22222)
    # grid_demo()
    # draw_bar_plays([110,20],123)
    # draw_line_playhobby()
    # print(pyecharts.__version__)
    # draw_pie_hobby()
    # data = [("古风",3),("古典",2),("电子",1),("民谣",5),("流行",3),("说唱",1),("摇滚",1)]
    # # draw_pie_plays([110,20],123)
    # draw_bar_like(data,123)