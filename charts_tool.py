from pyecharts import options as opts

from pyecharts.faker import Faker
from pyecharts.charts import Bar, Grid, Line, Pie,Tab

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
            .add_yaxis("用户:"+str(user_id), y,color=Faker.rand_color())
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             toolbox_opts=opts.ToolboxOpts()
                             )
            .render(file_name)
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
        Pie()
            .add(
            "",
            data,
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{b}: {d}% ",
            ),
            center=["40%", "50%"],
        )
            .set_global_opts(title_opts=opts.TitleOpts(title=title),

                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="60%", orient="vertical")
                             )
            .render(file_name)
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
                value=data[idx],
                itemstyle_opts=opts.ItemStyleOpts(color=color[idx]),
            )
        )
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("用户:" + str(user_id), y, color=Faker.rand_color())
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             toolbox_opts=opts.ToolboxOpts()
                             )
            .render(file_name)
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
            .render(file_name)
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
            center=["30%", "50%"],
        )
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="60%", orient="vertical")
                             )
            .render(file_name)
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
            .add_yaxis("用户:" + str(user_id), y, color=Faker.rand_color())
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             toolbox_opts=opts.ToolboxOpts()
                             )
            .render(file_name)
    )
    return c

def draw_cloud(url,user_id,title = "用户词云"):
    image = Image()
    img_src = (url)
    image.add(
        src=img_src,
        style_opts={"width": "200px", "height": "200px", "style": "margin-top: 20px"},
    )
    image.set_global_opts(
        title_opts=ComponentTitleOpts(title="Image-基本示例")
    )
    file_name = "user_data/" + str(user_id) + "_cloud.html"
    image.render(file_name)
    return image

def grid_demo():
    data = [("古风", 3), ("古典", 2), ("电子", 1), ("民谣", 5), ("流行", 3), ("说唱", 1), ("摇滚", 1)]
    pie = draw_pie_like(data,111)
    bar = draw_bar_like(data,111)
    grid = (
        Grid()
        .add(pie, grid_opts=opts.GridOpts(pos_bottom="60%"))
        .add(bar, grid_opts=opts.GridOpts(pos_top="60%"))
        .render("grid_horizontal.html")
    )




def tab_demo(user_id,title="用户数据分析"):
    tab = Tab()
    tab.add(bar_datazoom_slider(), "bar-example")
    tab.add(line_markpoint(), "line-example")
    tab.add(pie_rosetype(), "pie-example")
    tab.add(grid_mutil_yaxis(), "grid-example")
    tab.render("tab_base.html")



if __name__ == '__main__':
    print("-----")
    # bar_color_demo()
    # draw_bar_plays([10,130],111)
    # grid_demo()
    # draw_bar_plays([110,20],123)
    # draw_line_playhobby()
    # print(pyecharts.__version__)
    # draw_pie_hobby()
    data = [("古风",3),("古典",2),("电子",1),("民谣",5),("流行",3),("说唱",1),("摇滚",1)]
    # draw_pie_plays([110,20],123)
    draw_bar_like(data,123)