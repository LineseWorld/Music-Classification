from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Pie
import random
# 柱状图
def draw_bar_plays(plays,user_id,title="标题"):
    bar = Bar()
    bar.add_xaxis(["片段播放", "完整播放"])
    bar.add_yaxis("用户:"+str(user_id), plays)
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    bar.set_global_opts(title_opts=opts.TitleOpts(title="Bar-Brush示例", subtitle="我是副标题",pos_left="center"),
                        toolbox_opts=opts.ToolboxOpts(),
                        legend_opts=opts.LegendOpts(is_show=False),
                        yaxis_opts=opts.AxisOpts(name="我是 Y 轴"),
                        xaxis_opts=opts.AxisOpts(name="我是 X 轴"),
                        )
    file_name = "bar_plays.html"
    bar.render(file_name)


def draw_line_plays():

    # http://gallery.pyecharts.org/#/Line/basic_line_chart
    x_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    y_data = [820, 932, 901, 934, 1290, 1330, 1320]

    (
        Line()
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .render("basic_line_chart.html")
    )

    c = (
        Line()
            .add_xaxis(Faker.choose())
            .add_yaxis("商家A", Faker.values())
            .add_yaxis("商家B", Faker.values())
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
            .render("line_base.html")
    )


def draw_line_playhobby(playhobbys,user_id,title = "标题"):
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
            .render("line_playhobby.html")
    )

def draw_pie_hobby(data,user_id,title="标题"):
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
            .render("pie_hobby.html")
    )
if __name__ == '__main__':
    # draw_bar_plays([110,20],123)
    # draw_line_playhobby()
    # print(pyecharts.__version__)
    draw_pie_hobby()