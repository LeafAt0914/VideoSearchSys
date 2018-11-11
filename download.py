import subprocess
from tkinter import *
import threading

'''
下载类
完成下载、抽取音频、保存操作
'''
class Download():
	def start(self, yt_url, file_path, name, process):
		self.download_start(yt_url, file_path, name, process)

	def printerr(self, child):
		while True:
			buff = child.stderr.readline()
			if buff == '' or child.poll() != None:
				break
			self.process.configure(state = "normal")
			self.process.insert(END, buff.decode('gbk'))
			self.process.see(END) #焦点定在行尾
			self.process.configure(state = "disabled") #让文本框不可编辑
	#视频链接、保存路径、进度框（未实现）
	def download_start(self, yt_url, file_path, name, process):
		self.process = process
		#加入转义字符(在URL链接两边加上引号就可以避免格式的问题)
		#yt_url = yt_url.replace('&', "^&") #在yt_url中&之前加入转义字符^ 
		#构造命令
		command = "youtube-dl -k -x -f best --no-playlist --newline \""+yt_url+"\" -o "+file_path+"/"+name+".%(ext)s"
		#执行
		child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#child.wait() #阻塞父进程等待子进程
		th_err = threading.Thread(target = self.printerr,args=(child,))
		th_err.setDaemon(True) #主线程退出子线程也退出
		th_err.start()
		while True:  
			buff = child.stdout.readline()
			if child.poll() != None:
				break
			self.process.configure(state = "normal")
			self.process.insert(END, buff.decode('gbk'))
			self.process.see(END) #焦点定在行尾
			self.process.configure(state = "disabled") #让文本框不可编辑
		child.kill()
if __name__ == "__main__":
	pass
