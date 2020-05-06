import sys,app
import os
import tkinter as tk
from crawl_song import judge_user
import webbrowser
import time
import connect_sql
import tkinter.messagebox





def window1():
    # 窗口
    window = tk.Tk()
    window.title('用户行为分析系统')
    window.geometry('650x350')
    # welcome image
    canvas = tk.Canvas(window, height=200, width=650)  # 创建画布
    image_file = tk.PhotoImage(file='source\welcome.png')  # 加载图片文件
    image = canvas.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上
    canvas.pack(side='top')  # 放置画布（为上端）
    # 标签 用户名密码
    tk.Label(window, text='用户名:').place(x=170, y=200)
    tk.Label(window, text='密码:').place(x=170, y=240)
    # 用户名输入框
    var_usr_name = tk.StringVar()
    var_usr_name.set('网易云用户手机账号')  # 变量赋值'example@python.com'
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=230, y=200)
    # 密码输入框
    var_usr_pwd = tk.StringVar()
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=230, y=240)


    # 登录函数
    def usr_log_in():
        # 输入框获取用户名密码
        usr_name = var_usr_name.get()
        usr_pwd = var_usr_pwd.get()
        # 判断用户名和密码是否匹配
        user_id = judge_user(usr_name,usr_pwd)
        if user_id:
            window.destroy()
            window2(user_id)
        else:
            tk.messagebox.showerror(message='账号密码错误')

    def usr_sign_quit():
        window.destroy()
    #登录 注册按钮
    bt_login=tk.Button(window,text='登录',command=usr_log_in)
    bt_login.place(x=200,y=280)

    bt_logquit=tk.Button(window,text='退出',command=usr_sign_quit)
    bt_logquit.place(x=340,y=280)
    #主循环
    window.mainloop()



def window2(user_id):
    # 窗口
    window = tk.Tk()
    window.title('用户行为分析系统')
    window.geometry('450x200')
    tk.Label(window, text='欢迎，ID为'+str(user_id)+" 的用户！",font=("微软雅黑", 12)).place(x=0, y=0)
    tk.Label(window, text="录入用户数据", font=("微软雅黑", 10),fg='blue').place(x=250, y=30)
    tk.Label(window, text="数据可视化与处理", font=("微软雅黑", 10),fg='red').place(x=10, y=30)
    # 登录函数
    def usr_show():
        chromePath = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
        file_name = 'F:\\pyspace\\Graduation project\\user_data\\'+str(user_id)+'_data.html'
        webbrowser.get('chrome').open_new_tab(file_name)


    def usr_update():
        app.update_user_message(user_id)
        tk.messagebox.showinfo(title='提示', message='更新成功')


    def tag2():
        window_tag = tk.Toplevel(window)
        window_tag.geometry('350x220')
        window_tag.title('录入数据')
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        def insert_op():
            sql = connect_sql.SQL()
            # 输入的信息
            song = song_id.get()
            start = start_time.get()
            end = end_time.get()
            cnt = times.get()
            values = []
            values.append(user_id)
            values.append(song)
            values.append(2)
            values.append(start)
            values.append(end)
            values.append(cnt)
            values.append("message")
            values.append(datetime)
            sql.insert_recoder(values)
            tk.messagebox.showinfo(title='提示', message='插入成功')
            window_tag.destroy()

        song_id = tk.StringVar()  # 将输入的注册名赋值给变量
        tk.Label(window_tag, text='歌曲id: ').place(x=10, y=10)  # 将`User name:`放置在坐标（10,10）。
        entry_song_id = tk.Entry(window_tag, textvariable=song_id)  # 创建一个注册名的`entry`，变量为`new_name`
        entry_song_id.place(x=150, y=10)  # `entry`放置在坐标（150,10）.

        start_time = tk.StringVar()
        tk.Label(window_tag, text='开始时间: ').place(x=10, y=50)
        entry_start_time = tk.Entry(window_tag, textvariable=start_time)
        entry_start_time.place(x=150, y=50)

        end_time = tk.StringVar()
        tk.Label(window_tag, text='结束时间: ').place(x=10, y=90)
        entry_end_time = tk.Entry(window_tag, textvariable=end_time)
        entry_end_time.place(x=150, y=90)

        times = tk.StringVar()
        tk.Label(window_tag, text='播放次数: ').place(x=10, y=130)
        entry_times = tk.Entry(window_tag, textvariable=times)
        entry_times.place(x=150, y=130)

        # 下面的 sign_to_Mofan_Python 我们再后面接着说
        btn_tag = tk.Button(window_tag, text='录入', command=insert_op)
        btn_tag.place(x=150, y=170)

    def tag1():
        window_tag = tk.Toplevel(window)
        window_tag.geometry('350x130')
        window_tag.title('录入数据')
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        def insert_op():
            sql = connect_sql.SQL()
            # 输入的信息
            song = song_id.get()
            cnt = times.get()
            values = []
            values.append(user_id)
            values.append(song)
            values.append(1)
            values.append(0)
            values.append(0)
            values.append(cnt)
            values.append("message")
            values.append(datetime)
            sql.insert_recoder(values)
            tk.messagebox.showinfo(title='提示', message='插入成功')
            window_tag.destroy()

        song_id = tk.StringVar()
        tk.Label(window_tag, text='歌曲id: ').place(x=10, y=10)
        entry_song_id = tk.Entry(window_tag, textvariable=song_id)
        entry_song_id.place(x=150, y=10)
        times = tk.StringVar()
        tk.Label(window_tag, text='循环次数: ').place(x=10, y=50)
        entry_times = tk.Entry(window_tag, textvariable=times)
        entry_times.place(x=150, y=50)
        btn_tag = tk.Button(window_tag, text='录入', command=insert_op)
        btn_tag.place(x=150, y=90)

    def tag3():
        window_tag = tk.Toplevel(window)
        window_tag.geometry('350x170')
        window_tag.title('录入数据')
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        def insert_op():
            sql = connect_sql.SQL()
            # 输入的信息
            song = song_id.get()
            start = start_time.get()
            cnt = times.get()
            values = []
            values.append(user_id)
            values.append(song)
            values.append(3)
            values.append(0)
            values.append(start)
            values.append(cnt)
            values.append("message")
            values.append(datetime)
            sql.insert_recoder(values)
            tk.messagebox.showinfo(title='提示', message='插入成功')
            window_tag.destroy()

        song_id = tk.StringVar()
        tk.Label(window_tag, text='歌曲id: ').place(x=10, y=10)
        entry_song_id = tk.Entry(window_tag, textvariable=song_id)
        entry_song_id.place(x=150, y=10)

        start_time = tk.StringVar()
        tk.Label(window_tag, text='评论时长: ').place(x=10, y=50)
        entry_start_time = tk.Entry(window_tag, textvariable=start_time)
        entry_start_time.place(x=150, y=50)

        times = tk.StringVar()
        tk.Label(window_tag, text='评论次数: ').place(x=10, y=90)
        entry_times = tk.Entry(window_tag, textvariable=times)
        entry_times.place(x=150, y=90)

        # 下面的 sign_to_Mofan_Python 我们再后面接着说
        btn_tag = tk.Button(window_tag, text='录入', command=insert_op)
        btn_tag.place(x=150, y=130)


    def tag4():
        window_tag = tk.Toplevel(window)
        window_tag.geometry('350x130')
        window_tag.title('录入数据')
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        def insert_op():
            sql = connect_sql.SQL()
            # 输入的信息
            song = song_id.get()
            cnt = times.get()
            values = []
            values.append(user_id)
            values.append(song)
            values.append(4)
            values.append(0)
            values.append(0)
            values.append(cnt)
            values.append("message")
            values.append(datetime)
            sql.insert_recoder(values)
            tk.messagebox.showinfo(title='提示', message='插入成功')
            window_tag.destroy()

        song_id = tk.StringVar()
        tk.Label(window_tag, text='歌曲id: ').place(x=10, y=10)
        entry_song_id = tk.Entry(window_tag, textvariable=song_id)
        entry_song_id.place(x=150, y=10)
        times = tk.StringVar()
        tk.Label(window_tag, text='点赞次数: ').place(x=10, y=50)
        entry_times = tk.Entry(window_tag, textvariable=times)
        entry_times.place(x=150, y=50)
        btn_tag = tk.Button(window_tag, text='录入', command=insert_op)
        btn_tag.place(x=150, y=90)

    def tag5():
        window_tag = tk.Toplevel(window)
        window_tag.geometry('350x90')
        window_tag.title('录入数据')
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        def insert_op():
            sql = connect_sql.SQL()
            # 输入的信息
            song = song_id.get()
            cnt = times.get()
            values = []
            values.append(user_id)
            values.append(song)
            values.append(5)
            values.append(0)
            values.append(0)
            values.append(10)
            values.append("message")
            values.append(datetime)
            sql.insert_recoder(values)
            tk.messagebox.showinfo(title='提示', message='插入成功')
            window_tag.destroy()

        song_id = tk.StringVar()
        tk.Label(window_tag, text='歌曲id: ').place(x=10, y=10)
        entry_song_id = tk.Entry(window_tag, textvariable=song_id)
        entry_song_id.place(x=150, y=10)
        times = tk.StringVar()
        btn_tag = tk.Button(window_tag, text='收藏', command=insert_op)
        btn_tag.place(x=150, y=50)

    def usr_quit():
        window.destroy()
        print("退出程序后更新数据")
        app.update_user_message(user_id)
        window1()


    bt_show=tk.Button(window,text='  数据可视化 ',command=usr_show)
    bt_show.place(x=10,y=60)

    bt_update=tk.Button(window,text='更新用户信息',command=usr_update)
    bt_update.place(x=10,y=100)


    bt_tag1 = tk.Button(window, text='录入单曲循环行为', command=tag1)
    bt_tag1.place(x=180, y=60)

    bt_tag2 = tk.Button(window, text='录入片段播放行为', command=tag2)
    bt_tag2.place(x=300, y=60)

    bt_tag3 = tk.Button(window, text='录入查看评论行为', command=tag3)
    bt_tag3.place(x=180, y=100)

    bt_tag4 = tk.Button(window, text='录入点赞评论行为', command=tag4)
    bt_tag4.place(x=300, y=100)

    bt_tag5 = tk.Button(window, text='录入收藏歌曲行为', command=tag5)
    bt_tag5.place(x=240, y=140)

    bt_quit = tk.Button(window, text='退出登陆', command=usr_quit)
    bt_quit.place(x=360, y=160)

    #主循环
    window.mainloop()



if __name__ == '__main__':
    # 393361316
    window1()