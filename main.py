import app
import interface as it
import os

if __name__ == '__main__':

    cmd = 'node F:\\NeteaseCloudMusicApi\\NeteaseCloudMusicApi\\app.js'
    try:
        p = os.popen(cmd)
    except:
        print("已开启")

    it.window1()
