#!/usr/bin/env python

#apt install git;pip install git+https://github.com/dpallot/simple-websocket-server.git

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

def sendto(socket,action,Message,Frienduin,Senderuin,picPath):
    message_json = json.loads("{}");
    message_json['action'] = action;
    message_json['Message'] = Message;
    message_json['Frienduin'] = Frienduin;
    message_json['Senderuin'] = Senderuin;
    message_json['picPath'] = picPath;
    print(json.dumps(message_json));
    socket.sendMessage(json.dumps(message_json));

def onqqmessage(socket,Message,Frienduin,Senderuin,Istroop,Nickname,Selfuin,Time):
    #params onqqmessage(socket,Message,Frienduin,Senderuin,Istroop,Nickname,Selfuin,Time):
    #socket websocket对象
    #Message 消息内容
    #Frienduin 群qq号/好友qq号
    #Senderuin 发送者qq号
    #Istroop 1:群消息 1000:私聊 0:好友消息
    #Nickname 发送者昵称
    #Selfuin 机器人qq号
    #Time 消息时间
    if Message == "测试文本":
        #params sendto(socket,action,Message,Frienduin,Senderuin,picPath):
        #socket websocket对象
        #action "sendMsg":发送消息 ||"sendPicMsg":发送图片消息||sendCardMsg:发送卡片消息"
        #Message 消息内容
        #Frienduin 群号/好友号
        #Senderuin 未知是否必要
        #picPath 图片路径/卡片内容
        sendto(socket,"sendMsg","文本消息",Frienduin,Senderuin,"")
    elif Message == "测试卡片":
        sendto(socket,"sendCardMsg","",Frienduin,Senderuin,"<msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"酷狗音乐\" sourceMsgId=\"0\" url=\"\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"http://singerimg.kugou.com/uploadpic/softhead/400/20170426/20170426152155521.jpg\" src=\"http://fs.w.kugou.com/201809150140/0fe84be3831cea79c86d693e721f0e7b/G012/M07/01/09/rIYBAFUKilCAV55kADj2J33IqoI680.mp3\" /><title>Innocence</title><summary>Avril Lavigne</summary></item><source name=\"酷狗音乐\" icon=\"http://url.cn/4Asex5p\" url=\"http://url.cn/SXih4O\" action=\"app\" a_actionData=\"com.kugou.android\" i_actionData=\"tencent205141://\" appid=\"205141\" /></msg>")
    elif Message == "测试图片":
        sendto(socket,"sendPicMsg","",Frienduin,Senderuin,"/sdcard/1111.png")
    elif Message == "测试语音":
        sendto(socket,"sendVoiceMsg","",Frienduin,Senderuin,"/sdcard/11111.amr")

def MessageFactory(socket,data):
    print(data);
    message_json = json.loads(str(data));
    Message = message_json['Message'];
    Frienduin = message_json['Frienduin'];
    Istroop = message_json['Istroop'];
    Nickname = message_json['Nickname'];
    Selfuin = message_json['Selfuin'];
    Time = message_json['Time'];
    Senderuin = message_json['Senderuin'];
    onqqmessage(socket,Message,Frienduin,Senderuin,Istroop,Nickname,Selfuin,Time);

class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        #self.sendMessage(self.data)
        MessageFactory(self,self.data)
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 9999, SimpleEcho)
server.serveforever()
