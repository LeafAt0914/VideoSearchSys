import os
from tkinter import *

_folderPath = "D:/crawler"
_Q = "中国共产党"

'''
在指定文件夹下查找所有txt文件有无指定内容
'''

class Search():
    def __init__(self, folderPath, Q, process):
        self.process = process
        self.searchTxt(folderPath, Q)

    #检查Q是否是line的子串
    def compare(self, Q, line):
        for i in range(len(line)):
            if line[i] == Q[0]:
                for j in range(len(Q)):
                    if j == len(Q) - 1:
                        return 1
                    if i + j + 1 > len(line):
                        break
                    if line[i + j + 1] != Q[j + 1]:
                        break
        return 0

    def readTxt(self, filePath, Q):
        f = open(filePath)             # 返回一个文件对象  
        line = f.readline()             # 调用文件的 readline()方法  
        lines = 0  #符合的行数
        while line:  
            #print(line, end = '')
            if self.compare(Q, line) == 1: #找到符合条件的
                #print(filePath.rfind('\\'))
                videoName = filePath[filePath.rfind('\\') + 1 : filePath.rfind('.')]    #截取出视频文件名 '\\'是转义
                #print(videoName, line, end = "")
                if lines == 0:
                    self.process.configure(state = "normal")
                    self.process.insert(END, "\n[" + "视频文件名：" + videoName + "]\n" + '\n')
                    self.process.see(END) #焦点定在行尾
                    self.process.configure(state = "disabled") #让文本框不可编辑 
                self.process.configure(state = "normal")
                self.process.insert(END, line)
                self.process.see(END) #焦点定在行尾
                self.process.configure(state = "disabled") #让文本框不可编辑
                lines += 1
            line = f.readline()  
        f.close()   #关闭文件

    def searchTxt(self, folderPath, Q):
        files = os.listdir(folderPath)      #获取当前路径下的文件名，返回List
        for f in files:
            filePath = os.path.join(folderPath, f)     #将文件名加入到当前文件路径后面
            if os.path.isfile(filePath) :         #如果是文件
                if os.path.splitext(filePath)[1]==".txt":  #判断是否是txt
                    self.readTxt(filePath, Q)                     #读文件
        self.process.configure(state = "normal")
        self.process.insert(END, "\n[" + "检索完成！" + "]\n")
        self.process.see(END) #焦点定在行尾
        self.process.configure(state = "disabled") #让文本框不可编辑

if __name__ == "__main__":
    Search(_folderPath, _Q)
