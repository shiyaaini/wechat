from flask import Flask,request
import time,json,os,yaml
import flask_cors
# 解析xml数据
import xmltodict
from datetime import datetime
from threading import Thread
import event

app = Flask(__name__)
flask_cors.CORS(app)
@app.route('/callback',methods=["POST"])
def index():
    # print(request.json)
    p=request.json
    roomid=p['roomid']
    wxid=p['sender']
    sign=p['sign']
    # 过滤掉公众号和其他无关信息
    zhh=str(wxid).split('_')[0]
    if zhh !="wxid":
        print("公众号信息或者其他无关信息")
        return "success"



    # 获取发信息方
    if p['is_group']==True or p['is_group']==False:
        g = event.contacts()
        for i in g["data"]["contacts"]:
            if i['wxid'] == roomid:
                global user
                user = i['name']
                if p['is_group'] == True:
                    g = event.contacts()
                    for j in g["data"]["contacts"]:
                        if j["wxid"] == wxid:
                            global friend
                            friend = j['name']
            elif i['wxid'] == wxid and p['is_group'] == False:
                user = i['name']
    # 文本信息
    if p['type']==1:
        xml=xmltodict.parse(p["xml"])
        content=p['content']
        # 判断是否是群信息
        if p['is_group']==True:
            print(f"群聊：{user}>>{friend}>>{content}")
            users=event.user_info()
            # 判断是否是@信息
            group_msg=event.chatroom_member(roomid)

            bot_wxid=event.wxid()
            bot_wxid=bot_wxid["data"]["wxid"]
            gd=group_msg["data"]["members"][bot_wxid]
            if f'@{gd}'in p['content']:
                content=str(content).replace(f"@{users}",'')
                event.text(content,roomid)
            else:
                pass
        # 判断是否是私聊信息
        elif p['is_group']==False:
            print(f"私聊：{user}>>{content}")
            event.text(content, wxid)

        else:
            return "success"
    #     好友申请默认自动同意
    elif p['type']==37:
        xml=xmltodict.parse(p["content"])
        v3=xml['msg']['@encryptusername']
        v4=xml['msg']['@ticket']
        scene=xml['msg']['@scene']
        fromnickname=xml['msg']['@fromusername']
        content=xml['msg']['@content']
        print(f"好友申请：{fromnickname},申请备注{content}")
        event.new_friend(v3,v4,scene)
    # 转账自动收取
    elif p['type']==49:
        xml=xmltodict.parse(p["content"])

        if p["is_group"]==False:
            print(f'私人转账:{user}>>{xml["msg"]["appmsg"]["wcpayinfo"]["feedesc"]}')
        else:
            return "success"
        transcationid=xml["msg"]["appmsg"]["wcpayinfo"]["transcationid"]
        transferid=xml["msg"]["appmsg"]["wcpayinfo"]["transferid"]
        print(event.transfer(wxid,transferid,transcationid))
    else:
        return "success"
    return "success"

if __name__=="__main__":
    if not os.path.exists("config.yaml"):
        print("没有配置文件config.yaml，正在生成配置文件,可以自行修改参数")
        c={"wechat_bot":{"host":"127.0.0.1","port":8080}}
        with open("config.yaml","w",encoding="utf-8") as f:
            yaml.dump(c,f)

    with open("config.yaml",'r',encoding="utf-8")as f:
        config=yaml.safe_load(f)


    host=config["wechat_bot"]["host"]
    port=config["wechat_bot"]["port"]
    # 启动监听机器人
    # Thread(target=bot,daemon=True).start()
    app.run(debug=True,host=host,port=port)