import subprocess
import sys
import hashlib
from hashlib import sha1
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import os
from tkinter import *

#下面是ui需要传入的参数

_audio_filepath_pre = "D:/crawler/output3.m4a" #正反斜杠都可以
_app_id = "5b25bf7c"
_api_key = "52177f49d8ceae86afb548a1f9bc1202"

base_url = "ws://rtasr.xfyun.cn/v1/ws"
end_tag = "{\"end\": true}"

'''
转写类
完成转换音频格式、调用科大讯飞接口将音频转写为文本、保存文本、删除中间音频文件的功能
'''
class Transform():
    #调用ffmpeg,将音频文件转换为科大讯飞接口的输入格式
    def start(self, app_id, api_key, audio_filepath_pre, process):
        #print(threading.currentThread())
        self.process = process #不用传参数
        audiopath_midvalue = audio_filepath_pre[0 : audio_filepath_pre.rfind('.')] #截取掉后缀名
        #print(audiopath_midvalue)
        
        #构造命令
        #ffmpeg -y -i output.m4a -acodec pcm_s16le -f s16le -ac 1 -ar 16000 output.pcm
        self.process.configure(state = "normal")
        self.process.insert(END, "转换音频文件格式...\n")
        self.process.see(END) #焦点定在行尾
        self.process.configure(state = "disabled") #让文本框不可编辑
        command = "ffmpeg -y -i " + audio_filepath_pre + " -acodec pcm_s16le -f s16le -ac 1 -ar 16000 " + audiopath_midvalue + ".pcm"

        child = subprocess.Popen(command, shell=True) #执行
        child.wait() #貌似不能省掉，不省又会造成ui无响应(开子线程就可以了)，待解决（不等待转换完成无法发送文件）
        child.kill()
        self.header(app_id, api_key, audiopath_midvalue + ".txt", audiopath_midvalue + ".pcm")
    
    #生成权鉴参数
    def header(self, app_id, api_key, txt_filepath, audio_filepath):
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa)) #建立连接

        self.process.configure(state = "normal")
        self.process.insert(END, "转写中...\n")
        self.process.see(END) #焦点定在行尾
        self.process.configure(state = "disabled") #让文本框不可编辑

        self.trecv = threading.Thread(target=self.recv, args=(audio_filepath,))
        self.trecv.setDaemon(True)
        self.trecv.start()
        #打开写入文件
        self.fileHandle = open (txt_filepath, 'w' )
        #发送音频文件
        self.send(audio_filepath)

    #拼接当前句子的内容，返回片段ID、时间戳和内容
    def joint(self, data):
        jointResult = ""
        data_dict = json.loads(data)
        segId = data_dict["seg_id"]
        cn_dict = data_dict["cn"]
        st_dict = cn_dict["st"]
        rt_list = st_dict["rt"]
        startTime = st_dict["bg"]
        for i in range(len(rt_list)):
            ws_dict = rt_list[i]
            ws_list = ws_dict["ws"]
            for j in range(len(ws_list)):
                cw_dict = ws_list[j]
                cw_list = cw_dict["cw"]
                for k in range(len(cw_list)):
                    w_dict = cw_list[k]
                    w = w_dict["w"]
                    jointResult += w
        return segId, startTime, jointResult

    #发送音频文件
    def send(self, audio_filepath):
        file_object = open(audio_filepath, 'rb')
        try:
            index = 1
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                self.ws.send(chunk)

                index += 1
                time.sleep(0.04)
        finally:
            # print str(index) + ", read len:" + str(len(chunk)) + ", file tell:" + str(file_object.tell())
            file_object.close()

        self.ws.send(bytes(end_tag.encode('utf-8')))
        #print ("send end tag success")

    #接收返回的结果
    def recv(self, audio_filepath):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    #print ("receive result end")
                    break
                result_dict = json.loads(result) #json串转化为dict

                # 解析结果
                if result_dict["action"] == "started":
                    #print ("handshake success, result: " + result)
                    self.process.configure(state = "normal")
                    self.process.insert(END, "握手成功: " + result + '\n')
                    self.process.see(END) #焦点定在行尾
                    self.process.configure(state = "disabled") #让文本框不可编辑

                if result_dict["action"] == "result":
                    #print("rtasr result: " + result)
                    #print(result_dict["data"])
                    segId, startTime, words = self.joint(result_dict["data"])
                    #print(str(startTime) + " " + words)
                    if segId == 0: #第一个句子提前赋值
                        startTimepre = startTime
                        wordspre = words
                    if int(startTime)//100 != int(startTimepre)//100: #只保留同时间点最后的句子,整除100是因为时间戳的毫秒级误差
                        s = int(startTimepre) // 1000  #秒
                        ss = "%02d" % (s % 60)      #前补零
                        m = s // 60                 #分
                        mm = "%02d" % (m % 60)
                        h = m // 60                 #时
                        hh = "%02d" % h
                        #print(hh + ":" + mm + ":" + ss + "  " + wordspre)
                        self.fileHandle.write (hh + ":" + mm + ":" + ss + "  " + wordspre + '\n' ) #写入内容
                        
                        self.process.configure(state = "normal")
                        self.process.insert(END, hh + ":" + mm + ":" + ss + "  " + wordspre + '\n')
                        self.process.see(END) #焦点定在行尾
                        self.process.configure(state = "disabled") #让文本框不可编辑
                        
                    startTimepre = startTime
                    wordspre = words

                if result_dict["action"] == "error":
                    #print("rtasr error: " + result)
                    self.process.configure(state = "normal")
                    self.process.insert(END, "语音转写错误: " + result + '\n')
                    self.process.see(END) #焦点定在行尾
                    self.process.configure(state = "disabled") #让文本框不可编辑
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            #最后一个句子
            s = int(startTime) // 1000  #秒
            ss = "%02d" % (s % 60)      #前补零
            m = s // 60                 #分
            mm = "%02d" % (m % 60)
            h = m // 60                 #时
            hh = "%02d" % h
            #print(hh + ":" + mm + ":" + ss + "  " + words)
            self.fileHandle.write (hh + ":" + mm + ":" + ss + "  " + words + '\n' ) #写入内容
            
            self.process.configure(state = "normal")
            self.process.insert(END, hh + ":" + mm + ":" + ss + "  " + words + '\n')
            self.process.see(END) #焦点定在行尾
            self.process.configure(state = "disabled") #让文本框不可编辑
            self.process.configure(state = "normal")
            self.process.insert(END, "转写完成！\n")
            self.process.see(END) #焦点定在行尾
            self.process.configure(state = "disabled") #让文本框不可编辑
            
            #print("receive result end(closed)")
            self.fileHandle.close() #关闭文件
            os.remove(audio_filepath) #删除掉pcm文件

    #关闭链接
    def close(self):
        self.ws.close()
        #print("connection closed")
        self.process.configure(state = "normal")
        self.process.insert(END, "连接已断开.\n")
        self.process.see(END) #焦点定在行尾
        self.process.configure(state = "disabled") #让文本框不可编辑

if __name__ == "__main__":
    t = Transform(_app_id, _api_key, _audio_filepath_pre, process)

