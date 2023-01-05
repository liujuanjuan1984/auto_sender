"""
一个我在正式用的实例。
把本地文件夹下的内容，发送到 去中心微博 这个种子网络。
trx version 为 1，即现有的 quorum main 版本。
"""
from rum_auto_sender import AutoSender

local_dir_path = r"D:\MY-OBSIDIAN-DATA\my_weibo"

rum_group_seed = "rum://seed?v=1&e=0&n=0&b=fDLEJaQbSguWukji6IFjdQ&c=nZ4Tzjt39q4dpOXvFdlP8i535QncTjvdcPp0NfOpmSs&g=O7ejvtFFRK-Uz-ZLmS_48A&k=CAISIQKm%2BgTifqG6ga1FUb9NzXDetFIi9AosQSx%2FRBFH3RbGFQ%3D%3D&s=MEYCIQDlshiApdymHMDK65Qv9VqGevyspb3WW9cLcbHF0r7QagIhAMCxvEREmkQi2IReMu9OBx1rjSJvEcq510CywXYYsWHx&t=Fq-eR5Mpg6k&a=%E5%8E%BB%E4%B8%AD%E5%BF%83%E5%BE%AE%E5%8D%9A&y=group_timeline&u=http://101.42.141.118:62663?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwcyI6WyIzYmI3YTNiZS1kMTQ1LTQ0YWYtOTRjZi1lNjRiOTkyZmY4ZjAiXSwiZXhwIjoxODE3MzcwMTU0LCJuYW1lIjoiYWxsb3ctM2JiN2EzYmUtZDE0NS00NGFmLTk0Y2YtZTY0Yjk5MmZmOGYwIiwicm9sZSI6Im5vZGUifQ.q_wr0TjJsntEuFMeJSeOj6cpQGYFsdlLI4LlzTh-xJk"

bot = AutoSender(local_dir_path, rum_group_seed, rum_version=1)

txt = """
0 - byebye
1 - 上传本地修改到 rum group
2 - 从 rum group 下载最新到本地
3 - 从 rum group 下载最新到本地（其它目录）或新设备获取最新
4 - 更新个人信息
>>> 
"""

askuser = input(txt)
if askuser == "1":
    bot.auto_sender()
    print("上传本地修改到 rum group done.")
elif askuser == "2":
    bot.download_by_group()
    print("从 rum group 下载最新到本地 done.")
elif askuser == "3":
    bot.download_by_group("D:\\download")
    print("从 rum group 下载最新到本地（其它目录）或新设备获取最新 done.")
elif askuser == "4":
    bot.update_profile(name="大丸子", image=r"C:\Users\75801\Pictures\greebear1.jpg")
else:
    print("byebye!")
