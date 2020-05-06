import pymysql
import pandas as pd
from sqlalchemy import create_engine
import time
class SQL():
    # 初始化信息
    def __init__(self):
        # 使用 connect 方法，传入数据库地址，账号密码，数据库名就可以得到你的数据库对象
        self.address = "localhost"
        self.user = "root"
        self.password = "lsj123"
        self.db_name = "graduation"

    # 插入歌曲
    def insert_song(self, values):
        """
        插入歌曲
        :param values:sid,sname,sauthor,slrc,surl
        :return:
        """
        db = pymysql.connect(self.address, self.user, self.password, self.db_name,charset='utf8')
        # 插入一条记录
        ss = "("
        for i in range(0,5):
            ss=ss + "\'"+str(values[i])+"\'"
            if i == 4:
                ss=ss+")"
            else:
                ss=ss+","
        sql = "insert ignore into songs(song_id,song_name,song_author,song_lrc,song_url)" \
              " values "+ss

        # 接着我们获取 cursor 来操作我们的 pytest 这个数据库
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        print("成功插入数据")
        db.close()

    # 插入记录
    def insert_recoder(self, values):
        """
        插入用户数据
        :param values:uid,sid,tag,st,et,ts,me
        :return:
        """
        db = pymysql.connect(self.address, self.user, self.password, self.db_name,charset='utf8')
        # 插入一条记录
        ss = "("
        for i in range(0,8):
            ss=ss + "\'"+str(values[i])+"\'"
            if i == 7:
                ss=ss+")"
            else:
                ss=ss+","
        sql = "insert ignore into recoder(user_id,song_id,tag,start_time,end_time,times,message,inserttime) " \
              " values "+ss

        # 接着我们获取 cursor 来操作我们的 pytest 这个数据库
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        print("成功用户行为插入数据")
        db.close()

    # 获取记录
    def get_recoder_byUid(self,uid):
        """
        返回uid用户的recoder数据
        :param uid:user_id
        :return: pandas 类型
        """
        db =pymysql.connect(self.address, self.user, self.password, self.db_name,charset='utf8')
        sql = "select * from recoder where user_id="+"\'"+str(uid)+"\'"
        result = pd.read_sql_query(sql,con=db)
        # print(result)
        return result

    def get_songtabel(self):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        sql = "select song_id from songs ;"
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except:
            print("Error: unable to fecth data")
        # 关闭数据库连接
        db.close()

    def judge_user(self,user_id):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        sql = "select 1 from users where user_id = \'" + str(user_id) + "\' limit 1;"
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchone()
            return results
        except:
            print("Error: unable to fecth data")
        # 关闭数据库连接
        db.close()

    def get_user(self,user_id):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        sql = "select * from users where user_id=" + "\'" + str(user_id) + "\'"
        result = pd.read_sql_query(sql, con=db)
        # print(result)
        return result

    def insert_user(self,user_id):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ss = "(\'"+str(user_id)+"\', \'"+str(datetime)+"\')"
        sql = "insert ignore into users (user_id,lasttime) " \
              " values " + ss

        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        print("成功插入数据")
        db.close()


    def update_user(self,user_id,values):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        # 插入一条记录
        sql = "UPDATE users SET antique = %s ,classical = %s , electronic = %s , folk = %s , pop = %s , rap = %s , rock = %s , " \
              "lasttime = %s , songs= %s" \
              " WHERE user_id = "+str(user_id)
        val = tuple(values)

        cursor = db.cursor()
        cursor.execute(sql,val)
        db.commit()
        print("成功插入数据")
        db.close()

    def get_recoder_bydatetime(self,user_id,lasttime):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        sql = "select * from recoder where user_id =" + "\'" + str(user_id) + "\' and inserttime < \'"+str(lasttime)+"\'"
        result = pd.read_sql_query(sql, con=db)
        # print(result)
        return result

    # 判断歌曲库中是否存在
    def judgesong(self,song_id):
        db = pymysql.connect(self.address, self.user, self.password, self.db_name, charset='utf8')
        sql = "select 1 from songs where song_id = \'"+str(song_id)+"\' limit 1;"
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchone()
            return results
        except:
            print("Error: unable to fecth data")
        # 关闭数据库连接
        db.close()

if __name__ == '__main__':
    sql = SQL()
    # print(sql.get_songtabel())
    # sql.insert_user("13131")
    # print(sql.get_user("13131"))
    # datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # values = [1.0,2.0,3.0,4.0,5.0,7.0,8.0,datetime,100]
    # sql.update_user("13131",values)
    # print(sql.get_user("13131"))
    # lasttime = "2020-05-05 22:03:44"
    # print(sql.get_recoder_bydatetime("393361316",lasttime))