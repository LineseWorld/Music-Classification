import connect_sql,crawl_song,\
    edit_music,music_classify,visualization

# uid = 393361316

if __name__ == '__main__':
    sql = connect_sql.SQL()
    uid = "393361316"
    user_data = sql.get_recoder_byUid(uid)
    tag1_data = user_data.query("tag==1")
    tag2_data = user_data.query("tag==2")
    print(tag2_data)