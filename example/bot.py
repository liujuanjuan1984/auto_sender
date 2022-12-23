from rum_auto_sender import AutoSender

local_dir_path = r"D:\MY-OBSIDIAN-DATA\my_Schedule\2-写作库"

rum_group_seed = "rum://seed?v=1&e=0&n=0&c=V_U80S5mU3Sgh3X4cMUWDnDbKqYEiigadBV2CQ-Otus&g=KcN8sfl6TIir1IsACMwzvw&k=AgNvPTKxQ8nyjeeDAucpdFUNYVrszBF2xF_wo9TczIWp&s=qrCgEJKJ7amh7y3xi1jxpGhXwOOlJGSY6njxOyqDr9h_QIMS23wWWZ-XJ45fj2seKxQh3HzHcd1z3qUZQNDKoAE&t=FzMrileb5yI&a=auto_sender_test2&y=group_post&u=http%3A%2F%2F82.157.65.147%3A62726%3Fjwt%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwcyI6WyIyOWMzN2NiMS1mOTdhLTRjODgtYWJkNC04YjAwMDhjYzMzYmYiXSwiZXhwIjoxODI5NDA3NzYwLCJuYW1lIjoiYWxsb3ctMjljMzdjYjEtZjk3YS00Yzg4LWFiZDQtOGIwMDA4Y2MzM2JmIiwicm9sZSI6Im5vZGUifQ.Pzd-JjzmTEVHcysZGzPAROrg6iEQvb2IIThXCZ6rMpo"

bot = AutoSender(local_dir_path, rum_group_seed)

txt = """
0 - byebye
1 - 上传本地修改到 rum group
2 - 从 rum group 下载最新到本地
3 - 从 rum group 下载最新到本地（其它目录）或新设备获取最新
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
else:
    print("byebye!")
