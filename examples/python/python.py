#!/usr/bin/env python

#apt install git;pip install git+https://github.com/dpallot/simple-websocket-server.git

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json;
import re;
import pycurl;
import io;
from urllib.parse import quote;
import logging;

def Curl_Redirect(url):
    c = pycurl.Curl();
    c.setopt(pycurl.URL,url);
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36");
    c.setopt(pycurl.CUSTOMREQUEST,"GET");
    c.setopt(pycurl.FOLLOWLOCATION, 1);
    c.setopt(pycurl.TIMEOUT, 1000);
    body = io.BytesIO();
    c.setopt(pycurl.WRITEFUNCTION, body.write);
    c.perform();
    redirect_url=c.getinfo(pycurl.EFFECTIVE_URL);
    c.close;
    return redirect_url;


def Curl_Post(url,data):
    c = pycurl.Curl();
    c.setopt(pycurl.URL,url);
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36");
    c.setopt(pycurl.CUSTOMREQUEST,"POST");
    c.setopt(pycurl.POSTFIELDS,  data);
    c.setopt(pycurl.TIMEOUT, 1000);
    body = io.BytesIO();
    c.setopt(pycurl.WRITEFUNCTION, body.write);
    c.perform();
    html = body.getvalue();
    result=str(html,encoding = "utf8");
    c.close;
    return result;

def Curl_Get(url):
    c = pycurl.Curl();
    c.setopt(pycurl.URL,url);
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36");
    c.setopt(pycurl.CUSTOMREQUEST,"GET");
    c.setopt(pycurl.TIMEOUT, 1000);
    body = io.BytesIO();
    c.setopt(pycurl.WRITEFUNCTION, body.write);
    c.perform();
    html = body.getvalue();
    result=str(html,encoding = "utf8");
    c.close();
    return result;

def Netease_Music(song, position,mode):
    message_to_send ="";
    param = "hlpretag=<span class=\"s-fc2\">&hlposttag=</span>&s=" + quote(song.replace("\"","")) + "&offset=0&total=true&limit=10&type=1";
    info = Curl_Post("http://music.163.com/api/search/pc", param);
    songs_json = json.loads(info);
    songs_list = songs_json["result"]["songs"];
    songs_list_length = len(songs_list);
    if mode == 1:
        data = songs_list[position - 1];
        song_name = data["name"];
        song_id = data["id"];
        author_name = data["artists"][0]["name"];
        img = data["album"]["picUrl"];
        #String album_name =data.getJSONObject("album").getString("name");
        play_url = Curl_Redirect("http://music.163.com/song/media/outer/url?id=" + str(song_id) + ".mp3");
        if play_url == "http://music.163.com/404":
            message_to_send = "<msg serviceID=\"1\" brief=\"点歌失败\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">该歌曲无外链</title></item></msg>";
        else:
            message_to_send = "<msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"网易音乐\" sourceMsgId=\"0\" url=\"\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"" + img + "\" src=\"" + play_url + "\" /><title>" + song_name + "</title><summary>" + author_name + "</summary></item><source name=\"网易云音乐\" icon=\"https://url.cn/5TxJvzz\" url=\"http://url.cn/5pl4kkd\" action=\"app\" a_actionData=\"com.netease.cloudmusic\" i_actionData=\"tencent100495085://\" appid=\"205141\" /></msg>";
    elif mode == 2:
        time=0;
        while (time < songs_list_length):
            author_name = songs_list[time]["artists"][0]["name"];
            if re.match(position + ".*",author_name) != None: 
                message_to_send = Netease_Music(song, time + 1, 1);
                break;
            time=time+1;
        if message_to_send == "":
            message_to_send = "<msg serviceID=\"1\" brief=\"匹配失败\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">未匹配到指定歌手</title></item></msg>";
    elif mode == 3:
        xml="<msg serviceID=\"1\" templateID=\"1\" action=\"web\" brief=\"点歌列表\" url=\"\" flag=\"3\"><item layout=\"5\"><picture cover=\"https://i.loli.net/2018/10/02/5bb37e1e7d09b.png\"/></item><item layout=\"6\"><summary  color=\"#32CD32\" style=\"1\">";
        line ="<item><hr/></item>";
        time=0;
        while (time < songs_list_length):
            data = songs_list[time];
            song_name = data["name"];
            author_name = data["artists"][0]["name"];
            if len(song_name) >10:
                song_name = song_name[:10] + "...";
            if len(author_name) >20:
                author_name = author_name[:20] + "...";
            xml = xml + str(time + 1) + ":" + song_name + "   " + author_name +  "@@@#10;"
            time=time+1;
        message_to_send = xml + "</summary></item></msg>";
    return message_to_send;

def Kugou_Music(song, position,mode):
    message_to_send ="";
    info = Curl_Get("http://songsearch.kugou.com/song_search_v2?keyword=" + quote(song) + "&page=0&pagesize=10&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0");
    songs_json = json.loads(info);
    songs_list = songs_json["data"]["lists"];
    songs_list_length = len(songs_list);
    if mode == 1:
        File_hash = songs_list[position -1]["FileHash"];
        data = json.loads(Curl_Get("http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + File_hash))["data"];
        img = data["img"];
        author_name = data["author_name"];
        song_name = data["song_name"];
        play_url = data["play_url"];
        message_to_send = "<msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"酷狗音乐\" sourceMsgId=\"0\" url=\"\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"" + img + "\" src=\"" + play_url + "\" /><title>" + song_name + "</title><summary>" + author_name + "</summary></item><source name=\"酷狗音乐\" icon=\"http://url.cn/4Asex5p\" url=\"http://url.cn/SXih4O\" action=\"app\" a_actionData=\"com.kugou.android\" i_actionData=\"tencent205141://\" appid=\"205141\" /></msg>";
    elif mode == 2:
        time=0;
        while (time < songs_list_length):
            author_name = songs_list[time]["SingerName"];
            if re.match(position + ".*",author_name) != None: 
                message_to_send = Kugou_Music(song, time + 1, 1);
                break;
            time=time+1;
        if message_to_send == "":
            message_to_send = "<msg serviceID=\"1\" brief=\"匹配失败\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">未匹配到指定歌手</title></item></msg>";
    elif mode == 3:
        xml="<msg serviceID=\"1\" templateID=\"1\" action=\"web\" brief=\"点歌列表\" url=\"\" flag=\"3\"><item layout=\"5\"><picture cover=\"https://i.loli.net/2018/10/02/5bb37e1e7d09b.png\"/></item><item layout=\"6\"><summary  color=\"#32CD32\" style=\"1\">";
        line ="<item><hr/></item>";
        time=0;
        while (time < songs_list_length):
            File_hash = songs_list[time]["FileHash"];
            song_detail_json = json.loads(Curl_Get("http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + File_hash))["data"];
            img = song_detail_json["img"];
            author_name = song_detail_json["author_name"];
            song_name = song_detail_json["song_name"];
            if len(song_name) >10:
                song_name = song_name[:10] + "...";
            if len(author_name) >20:
                author_name = author_name[:20] + "...";
            xml = xml + str(time + 1) + ":" + song_name + "   " + author_name +  "@@@#10;"
            time=time+1;
        message_to_send = xml + "</summary></item></msg>";
    return message_to_send;

def sendto(socket,action,Message,Frienduin,Senderuin,picPath):
    message_json = json.loads("{}");
    message_json['action'] = action;
    message_json['Message'] = Message;
    message_json['Frienduin'] = Frienduin;
    message_json['Senderuin'] = Senderuin;
    message_json['picPath'] = picPath;
    print("发送消息到: \033[0m \033[32m"+Frienduin+"\033[0m 消息: \033[31m"+Message+picPath+"\033[0m\n");
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
    elif re.match("^网易点歌 .*",Message) != None:
        song="";
        singer="";
        song_list="false";
        song_position="false";
        singer_really_contented="false";
        message_to_send="";
        message_list=re.split("\s+",Message);
        if len(message_list) >= 2:
            song = message_list[1].replace("_", " ");
        if len(message_list) >= 3:
            singer = message_list[2].replace("_", " ");
            if re.match("[0-9]",singer) == None:
                singer_really_contented = "true";
            else:
                position = int(singer);
                song_position = "true";
        else:
            song_list="true";
        if song_position == "true":
            if position != 0:
                message_to_send = Netease_Music(song, position, 1);
            else:
                message_to_send = "<msg serviceID=\"33\" brief=\"格式错误\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">序号必须大于0</title></item></msg>";
        elif singer_really_contented == "true":
            message_to_send = Netease_Music(song, singer, 2);
        elif song_list == "true":
            message_to_send = Netease_Music(song, singer, 3);
            message_to_send = message_to_send.replace("&", "&amp;").replace("@@@", "&");
        sendto(socket,"sendCardMsg","",Frienduin,Senderuin,message_to_send);
    elif re.match("^酷狗点歌 .*",Message) != None:
        song="";
        singer="";
        song_list="false";
        song_position="false";
        singer_really_contented="false";
        message_to_send="";
        message_list=re.split("\s+",Message);
        if len(message_list) >= 2:
            song = message_list[1].replace("_", " ");
        if len(message_list) >= 3:
            singer = message_list[2].replace("_", " ");
            if re.match("[0-9]",singer) == None:
                singer_really_contented = "true";
            else:
                position = int(singer);
                song_position = "true";
        else:
            song_list="true";
        if song_position == "true":
            if position != 0:
                message_to_send = Kugou_Music(song, position, 1);
            else:
                message_to_send = "<msg serviceID=\"33\" brief=\"格式错误\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">序号必须大于0</title></item></msg>";
        elif singer_really_contented == "true":
            message_to_send = Kugou_Music(song, singer, 2);
        elif song_list == "true":
            message_to_send = Kugou_Music(song, singer, 3);
            message_to_send = message_to_send.replace("&", "&amp;").replace("@@@", "&");
        sendto(socket,"sendCardMsg","",Frienduin,Senderuin,message_to_send);


def MessageFactory(socket,data):
    message_json = json.loads(str(data));
    Message = message_json['Message'];
    Frienduin = message_json['Frienduin'];
    Istroop = message_json['Istroop'];
    Nickname = message_json['Nickname'];
    Selfuin = message_json['Selfuin'];
    Time = message_json['Time'];
    Senderuin = message_json['Senderuin'];
    if Istroop == 1:
        print("收到群消息 来自群: \033[0m \033[32m"+Frienduin+"\033[0m 的成员: \033[36m"+Nickname+"\033[0m 的消息: \033[31m"+Message+"\033[0m\n");
    elif Istroop == 0:
        print("收到好友消息 来自: "+Nickname+" 的消息: "+Message+"\n");
    elif Istroop == 1000:
        print("私聊消息 来自: "+Nickname+" 的消息: "+Message+"\n");
    onqqmessage(socket,Message,Frienduin,Senderuin,Istroop,Nickname,Selfuin,Time);

class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        #self.sendMessage(self.data)
        try:
            MessageFactory(self,self.data)
        except:
            logging.exception('error during handling user data')
            self.close(status=1011, reason='Internal server error')

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 9999, SimpleEcho)
server.serveforever()
