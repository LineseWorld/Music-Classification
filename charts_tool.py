from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Pie
import random
# 柱状图
def draw_bar_plays(plays,user_id,title="听歌方式"):
    """
    两种听歌方式
    :param plays:
    :param user_id:
    :param title:
    :return:
    """
    file_name = "user_data/" + str(user_id) + "_bar_plays.html"
    bar = Bar()
    bar.add_xaxis(["片段播放", "完整播放"])
    bar.add_yaxis("用户:"+str(user_id), plays)
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title,pos_left="center"),
                        toolbox_opts=opts.ToolboxOpts(),
                        legend_opts=opts.LegendOpts(is_show=False),
                        yaxis_opts=opts.AxisOpts(name="次数"),
                        # xaxis_opts=opts.AxisOpts(name="x"),
                        )
    bar.render(file_name)
    return bar

def draw_pie_recoder(data,user_id,title="用户行为占比"):
    """
    用户行为占比-未完成
    :param plays:
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
            center=["30%", "50%"],
        )
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="60%", orient="vertical")
                             )
            .render(file_name)
    )
    return c

def draw_bar_recoder(data,user_id,title = "用户行为统计"):
    return None

def draw_line_clip(playhobbys,user_id,title = "片段播放习惯"):
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
            playhobbys,
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
    lable = ["古风","古典","电子","民谣","流行","说唱","摇滚"]
    bar = Bar()
    bar.add_xaxis(lable)
    plays= []
    for i in range(7):
        plays.append(data[i][1])
    bar.add_yaxis("用户听歌曲风统计", plays)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title, pos_left="center"),
                        toolbox_opts=opts.ToolboxOpts(),
                        legend_opts=opts.LegendOpts(is_show=False),

                        )
    bar.render(file_name)
    return bar

if __name__ == '__main__':
    # draw_bar_plays([110,20],123)
    # draw_line_playhobby()
    # print(pyecharts.__version__)
    # draw_pie_hobby()
    data = [("古风",3),("古典",2),("电子",1),("民谣",5),("流行",3),("说唱",1),("摇滚",1)]
    draw_pie_plays([110,20],123)
    # draw_bar_like(data,123)