import requests,json,time,os,yaml
urls=f"http://127.0.0.1:9999"

# 获取登录账号个人信息
def user_info():
    resp=requests.get(f"{urls}/user-info")
    return json.loads(resp.text)
#获取登录状态
def login():
    resp=requests.get(f"{urls}/login")
    return json.loads(resp.text)
# 获取登录账号
def wxid():
    resp=requests.get(f"{urls}/wxid")
    return json.loads(resp.text)
# 获取信息类型
def msg_types():
    resp=requests.get(f"{urls}/msg-types")
    return json.loads(resp.text)
# 获取完整通讯录
def contacts():
    resp=requests.get(f"{urls}/contacts")
    return json.loads(resp.text)
# 获取所有好友列表
def friends():
    resp=requests.get(f"{urls}/friends")
    return json.loads(resp.text)
# 获取所有数据库
def dbs():
    resp=requests.get(f"{urls}/dbs")
    return json.loads(resp.text)
# 获取某个表的数据
def tables(db):
    resp=requests.get(f"{urls}/{db}/tables")
    return json.loads(resp.text)
# 刷新朋友圈
def pyq(id):
    params={"id":id}
    resp=requests.get(f"{urls}/pyq",params=params)
    return json.loads(resp.text)
# 获取群成员
def chatroom_member(roomid):
    # params = {"roomid": roomid}
    resp=requests.get(f"{urls}/chatroom-member/?roomid={roomid}")
    return json.loads(resp.text)
# 获取群成员名片
def alias_in_chatroom(roomid,wxid):
    params={"roomid":roomid,"wxid":wxid}
    resp=requests.get(f"{urls}/alias-in-chatroom",params=params)
    return json.loads(resp.text)
# 发送文本发信息
def text(msg,receiver,aters=""):
    """
    :param msg: 文本信息
    :param receiver: 接受信息用户
    :param aters:
    :return:
    """
    data={
      "msg": msg,
      "receiver": receiver,
      "aters": aters
    }
    resp=requests.post(f"{urls}/text",json=data)
    return json.loads(resp.text)
# 发送图片信息
def image(path,receiver):
    """

    :param path: 图片路径，如：“D:/git/wechat/1.jpg”
    :param receiver:接收信息用户
    :return:
    """
    data={
      "path": path,
      "receiver": receiver
    }
    resp=requests.post(f"{urls}/image",json=data)
    return json.loads(resp.text)
# 发送文件信息
def file(path,receiver):
    """

    :param path: 文件路径
    :param receiver: 接收文件用户
    :return:
    """
    data={
      "path": path,
      "receiver": receiver
    }
    resp=requests.post(f"{urls}/file",json=data)
    return json.loads(resp.text)
# 执行sql，如果数据量大注意分页，以免oom
def sql(db,sql):
    """

    :param db: 要查询的数据库
    :param sql:要执行的 SQL
    :return:
    """
    data={
        "db":db,
        "sql":sql
    }
    resp=requests.post(f"{urls}/sql",json=data)
    return json.loads(resp.text)
# 通过好友申请
def new_friend(v3,v4,scene):
    """

    :param v3:加密用户名 (好友申请消息里 v3 开头的字符串)
    :param v4:Ticket (好友申请消息里 v4 开头的字符串)
    :param scene:申请方式 (好友申请消息里的 scene)
    :return:
    """
    data={
      "v3": v3,
      "v4": v4,
      "scene": scene
    }
    resp=requests.post(f"{urls}/new-friend",json=data)
    return json.loads(resp.text)
#添加群成员
def push_member(roomid,wxids):
    """

    :param roomid: 群ID
    :param wxids: 用户ID
    :return:
    """
    data={
      "roomid": roomid,
      "wxids": wxids
    }
    resp=requests.post(f"{urls}/chatroom-member",json=data)
    return json.loads(resp.text)
# 删除群成员
def delete_member(roomid,wxid):
    """

    :param roomid: 群ID
    :param wxid: 要删除的 wxid，多个用逗号分隔
    :return:
    """
    data={
      "roomid": roomid,
      "wxid": wxid
    }
    resp=requests.delete(f"{urls}/delete-member",json=data)
    return json.loads(resp.text)
# 接收转账
def transfer(wxid,transferid,transactionid):
    """

    :param wxid: 转账消息里的发送人
    :param transferid:转账消息里的 transferid
    :param transactionid:转账信息里的transactionid
    :return:
    """
    data={
      "wxid": wxid,
      "transferid": transferid,
      "transactionid": transactionid
    }
    resp=requests.post(f"{urls}/transfer",json=data)
    return json.loads(resp.text)
# 解密图片
def dec_image(src,dst):
    """

    :param src:加密的图片路径
    :param dst:解密的图片路径
    :return:
    """
    data={
        "src": src,
        "dst": dst
    }
    resp=requests.post(f"{urls}/dec-image",json=data)
    return json.loads(resp.text)

# roomid="49592760706@chatroom"
# wxids="wxid_ekqp0hghdznh22"
# print(file("C:\\Users\Administrator\Pictures\\th.gif",wxids))