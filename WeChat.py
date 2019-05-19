import itchat
# import全部消息类型
from itchat.content import *

'''
@itchat.msg_register([], isFriendChat=True/False, isGroupChat=True/False,isMpChat=True/False)

#Wechat中的消息来源
isFriendChat表示好友之间，isGroupChat表示群聊，isMapChat表示公众号

#itcaht.content 中包含所有的消息类型参数：
—————————————————————————————————————————————————————————————————
参数         |  类型      |  Text 键值
TEXT        |  文本      |   文本内容(文字消息)
MAP         |  地图      |   位置文本(位置分享)
CARD        |  名片      |   推荐人字典(推荐人的名片)
SHARING     |  分享      |   分享名称(分享的音乐或者文章等)
PICTURE     |  图片/表情 |   下载方法                                 
RECORDING   |  语音      |  下载方法
ATTACHMENT  |  附件      |  下载方法
VIDEO       |  小视频    |  下载方法
FRIENDS     |  好友邀请   |   添加好友所需参数
SYSTEM      |  系统消息   |   更新内容的用户或群聊的UserName组成的列表
NOTE        |  通知      |   通知文本(消息撤回等)
—————————————————————————————————————————————————————————————————

#一般的消息都遵循以下的内容：
{
  "Text": "",                 <---     键值不定，可能是文本内容，下载方法等，具体如上表
  "Type": "",                 <---     消息类型，具体如上表
  "FromUserName": "",         <---     发送者
  "ToUserName": "",           <---     接收者
  "FileName": "",             <---     文件名
  "FileSize": "",             <---     文件大小
  "CreateTime": 0,
  "MsgId": "",
  
  #分享链接
  "Url": 链接地址
  
  #群消息
  "isAt": "",                 <---     判断是否 @ 本号
  "ActualNickName": ""        <---     实际 NickName(昵称)
  
  #名片消息
  "RecommendInfo":
   {
     "UserName": "xxx", # ID，这里的是昵称
     "Province": "xxx",  
     "City": "xxx",  
     "Scene": 17, 
     "QQNum": 0, 
     "Content": "", 
     "Alias": "xxx", # 微信号
     "OpCode": 0, 
     "Signature": "", 
     "Ticket": "", 
     "Sex": 0, # 1:男, 2:女
     "NickName": "xxx", # 昵称
     "AttrStatus": 4293221, 
     "VerifyFlag": 0
   }
   
   #地理位置消息
   "OriContent":
    "
    <?xml version="1.0"?>
    <msg>    
        <location x="34.195278" y="117.177803" scale="16" label="江苏省徐州市铜山区新区海河路" maptype="0" poiname="江苏师范大学大学生公寓园区" />   
    </msg>
    "
   
    "Content": "",
}
'''


# 处理文本类消息
# 包括文本、位置、名片、通知、分享
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    # msg['FromUserName']就是发送者的ID
    # 将消息的类型和文本内容返回给发送者，'filehelper'表示文件传输助手
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


# 处理多媒体类消息
# 包括图片、录音、文件、视频
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # msg['Text']是一个文件下载函数
    # 传入文件名，将文件下载下来
    msg['Text'](msg['FileName'])
    # 把下载好的文件再发回给发送者
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


# 处理好友添加请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    # 加完好友后，给好友打个招呼
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


# callback after successfully logged in
def lc():
    print("Finish Login!")


# callback after logged out
def ec():
    print("exit")


# 在auto_login()里面提供一个True，即hotReload=True
# 即可保留登陆状态
# 即使程序关闭，一定时间内重新开启也可以不用重新扫码
# 如果不添加参数enableCmdQR的话，就会作为图片显示，如果参数为True的话，就会在控制台显示
itchat.auto_login(enableCmdQR=True, hotReload=True, loginCallback=lc, exitCallback=ec)
# itchat.login() == itchat.auto_login(hotReload=False)

# 绑定消息响应事件后，让itchat运行起来，监听消息
itchat.run()

"""friend["UserName"]
itchat.send_msg("你好", ToUserName=)
itchat.send_image("xiaoqiao.jpeg", ToUserName=)
itchat.send_file("xiaoqiao.jpeg", ToUserName=)
itchat.send_video("你好.mp4".decode("utf-8"), ToUserName=)


#如果单纯的使用send函数，需要对发送内容进行标注。
@fil@：在发送内容前添加，表明是发送文件
@img@：在发送内容前添加，表明是图片文件
@msg@：在发送内容前添加，表明是消息
@vid@：在发送内容前添加，表明是视频文件，视频文件要小于20M
#如果什么都没有添加，默认是消息    
#toUserName是发送对象, 如果留空, 将发送给自己

itchat.send("@type@name", ToUserName=)

"""
