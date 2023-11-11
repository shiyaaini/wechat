import os,yaml
from threading import Thread
def bots():
    os.system(f"wcfhttp --cb http://{host}:{port}/callback")

if __name__ == '__main__':
    if not os.path.exists("config.yaml"):
        print("没有配置文件config.yaml，正在生成配置文件,可以自行修改参数")
        c={"wechat_bot":{"host":"127.0.0.1","port":8080}}
        with open("config.yaml","w",encoding="utf-8") as f:
            yaml.dump(c,f)

    with open("config.yaml",'r',encoding="utf-8")as f:
        config=yaml.safe_load(f)
    host=config["wechat_bot"]["host"]
    port=config["wechat_bot"]["port"]
    bots()
