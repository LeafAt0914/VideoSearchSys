from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from download import Download
from transform import Transform
from search import Search
import threading
#from tkinter.font import Font
#from tkinter.messagebox import *
#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog

#应用名称
application_title = "视频检索系统[版本:Beta]"

'''
应用主类，由它来调用其他各类
'''
class Application_ui(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)

        #各个输入框的值
        self.v_download_URL = StringVar()
        self.v_download_savepath = StringVar()
        self.v_download_rename = StringVar()
        self.v_transform_appid = StringVar()
        self.v_transform_apikey = StringVar()
        self.v_transform_audiopath = StringVar()
        self.v_search_keywords = StringVar()
        self.v_search_folder = StringVar()
        #self.v_download_process = StringVar

        self.master.title(application_title)
        self.master.geometry()
        self.master.resizable(width = False, height = False)
        self.createWidgets()

    #选择下载保存路径
    def download_savebrowse_callback(self):
        download_savepath = tkinter.filedialog.askdirectory() #调用文件夹选择框
        self.v_download_savepath.set(download_savepath)

    #开始下载
    def download_OK_callback(self):
        download_savepath = self.v_download_savepath.get()
        download_URL = self.v_download_URL.get()
        download_rename = self.v_download_rename.get()
        download_rename = download_rename.replace(" ", "")
        if download_URL == "":                                  #链接和保存路径均不能为空
            self.t_download_process.configure(state = "normal")
            self.t_download_process.insert(END, "请输入视频链接!\n")
            self.t_download_process.see(END)
            self.t_download_process.configure(state = "disabled")
        elif download_savepath == "":
            self.t_download_process.configure(state = "normal")
            self.t_download_process.insert(END, "请选择视频保存路径!\n")
            self.t_download_process.see(END)
            self.t_download_process.configure(state = "disabled")
        elif download_rename == "":
            self.t_download_process.configure(state = "normal")
            self.t_download_process.insert(END, "请给视频命名!\n")
            self.t_download_process.see(END)
            self.t_download_process.configure(state = "disabled")
        else:
            #self.t_download_process.insert(END, "连接YouTube URL中...\n")
            #开启下载线程
            self.ent_download_rename.delete(0, END)
            D = Download()
            th_download = threading.Thread(target = D.start,args=(download_URL,download_savepath,download_rename,self.t_download_process,))
            th_download.setDaemon(True) #主线程退出子线程也退出
            th_download.start()
            #Download(download_URL, download_savepath, self.t_download_process)
    
    def download_clear_callback(self):
        self.t_download_process.configure(state = "normal")
        self.t_download_process.delete(1.0, END)
        self.t_download_process.configure(state = "disabled")
    
    def transform_audiobrowse_callback(self):
        #调用文件选择框,选择特定文件
        transform_audiopath = tkinter.filedialog.askopenfilename(filetypes = (("audio files","*.ogg;*.m4a"),("all files","*.*")))
        self.v_transform_audiopath.set(transform_audiopath)
    
    def transform_OK_callback(self):
        transform_appid = self.v_transform_appid.get()
        transform_apikey = self.v_transform_apikey.get()
        transform_audiopath = self.v_transform_audiopath.get()
        if transform_appid == "":
            self.t_transform_process.configure(state = "normal")            
            self.t_transform_process.insert(END, "请输入APPID!\n")
            self.t_transform_process.see(END)
            self.t_transform_process.configure(state = "disabled")
        elif transform_apikey == "":
            self.t_transform_process.configure(state = "normal")              
            self.t_transform_process.insert(END, "请输入APIkey!\n")
            self.t_transform_process.see(END)
            self.t_transform_process.configure(state = "disabled")
        elif transform_audiopath== "":
            self.t_transform_process.configure(state = "normal") 
            self.t_transform_process.insert(END, "请选择音频文件!\n")
            self.t_transform_process.see(END)
            self.t_transform_process.configure(state = "disabled")
        else:
            #调用转写模块
            T = Transform()
            th_transform = threading.Thread(target = T.start,args=(transform_appid,transform_apikey,transform_audiopath,self.t_transform_process,))
            th_transform.setDaemon(True)
            th_transform.start()
            #T.start(transform_appid, transform_apikey, transform_audiopath, self.t_transform_process)

    def transform_clear_callback(self):
        self.t_transform_process.configure(state = "normal")
        self.t_transform_process.delete(1.0, END)
        self.t_transform_process.configure(state = "disabled")

    def search_folderbrowse_callback(self):
        search_folder = tkinter.filedialog.askdirectory() #调用文件夹选择框
        self.v_search_folder.set(search_folder)

    def search_OK_callback(self):
        search_keywords = self.v_search_keywords.get()
        search_keywords = search_keywords.replace(" ", "") #去掉空格
        search_folder = self.v_search_folder.get()
        if search_keywords == "":
            self.t_search_process.configure(state = "normal") 
            self.t_search_process.insert(END, "请输入待检索关键词!\n")
            self.t_search_process.see(END)
            self.t_search_process.configure(state = "disabled")
        elif search_folder == "":
            self.t_search_process.configure(state = "normal") 
            self.t_search_process.insert(END, "请选择待检索文件夹!\n")
            self.t_search_process.see(END)
            self.t_search_process.configure(state = "disabled")
        else:
            Search(search_folder, search_keywords, self.t_search_process)

    def search_clear_callback(self):
        self.t_search_process.configure(state = "normal") 
        self.t_search_process.delete(1.0, END)
        self.t_search_process.configure(state = "disabled")

    #创建UI界面
    def createWidgets(self):
        self.root = self.winfo_toplevel()
 
        self.style = Style()
 
        self.topwin = Notebook(self.root)
        self.topwin.pack()

        #下载版块
        self.frm_download = Frame(self.topwin)
        #定义组件
        self.lbl_download_URL = Label(self.frm_download, text='视频链接')
        self.ent_download_URL = Entry(self.frm_download, textvariable = self.v_download_URL)
        self.lbl_download_savepath = Label(self.frm_download, text='保存路径')
        self.ent_download_savepath = Entry(self.frm_download, textvariable = self.v_download_savepath)
        self.btn_download_browse = Button(self.frm_download, text = "浏览", command = self.download_savebrowse_callback)
        self.lbl_download_rename = Label(self.frm_download, text="重命名")
        self.ent_download_rename = Entry(self.frm_download, textvariable = self.v_download_rename)
        #self.lbl_download_tip = Label(self.frm_download, text="不重命名不要作输入")
        self.btn_download_OK = Button(self.frm_download, text = "确定", command = self.download_OK_callback)
        self.btn_download_clear = Button(self.frm_download, text = "清屏", command = self.download_clear_callback)
        self.lfrm_download_process = LabelFrame(self.frm_download, text = "进度")
        self.t_download_process = Text(self.lfrm_download_process, state="disabled") #不可编辑
        self.sb_download_bar = Scrollbar(self.lfrm_download_process) #滚动条创建
        self.t_download_process["yscrollcommand"] = self.sb_download_bar.set #滚动条绑定
        self.sb_download_bar.config(command = self.t_download_process.yview) #滚动条绑定
        #放置
        self.lbl_download_URL.grid(row = 0, column = 0)
        self.ent_download_URL.grid(row = 0, column = 1, columnspan = 2, sticky = W + E)
        self.lbl_download_savepath.grid(row = 1, column = 0)
        self.ent_download_savepath.grid(row = 1, column = 1, sticky = W + E)
        self.btn_download_browse.grid(row = 1, column = 2, sticky = W)
        self.lbl_download_rename.grid(row = 2, column = 0)
        self.ent_download_rename.grid(row = 2, column = 1, columnspan = 2, sticky = W + E)
        #self.lbl_download_tip.grid(row = 2, column = 3, sticky = W)
        self.btn_download_OK.grid(row = 3, column = 1)
        self.btn_download_clear.grid(row = 3, column = 3, sticky = E)
        self.lfrm_download_process.grid(row = 4, column = 0, columnspan = 4)
        self.t_download_process.grid(row =0, column = 0)
        self.sb_download_bar.grid(row = 0, column = 1, sticky = E + N + S) #滚动条放置
        #加入Notebook
        self.topwin.add(self.frm_download, text = '下载视频')

        #语音转写版块
        self.frm_transform = Frame(self.topwin)

        self.lbl_transform_appid = Label(self.frm_transform, text="APPID")
        self.ent_transform_appid = Entry(self.frm_transform, textvariable = self.v_transform_appid)
        self.lbl_transform_apikey = Label(self.frm_transform, text="APIkey")
        self.ent_transform_apikey = Entry(self.frm_transform, textvariable = self.v_transform_apikey)
        self.lbl_transform_audiopath = Label(self.frm_transform, text="音频文件")
        self.ent_transform_audiopath = Entry(self.frm_transform, textvariable = self.v_transform_audiopath)
        self.btn_transform_audiobrowse = Button(self.frm_transform, text = "浏览", command = self.transform_audiobrowse_callback)
        self.btn_transform_OK = Button(self.frm_transform, text = "确定", command = self.transform_OK_callback)
        self.btn_transform_clear = Button(self.frm_transform, text = "清屏", command = self.transform_clear_callback)
        self.lfrm_transform_process = LabelFrame(self.frm_transform, text = "进度")
        self.t_transform_process = Text(self.lfrm_transform_process, state="disabled")
        self.sb_transform_bar = Scrollbar(self.lfrm_transform_process) #滚动条创建
        self.t_transform_process["yscrollcommand"] = self.sb_transform_bar.set #滚动条绑定
        self.sb_transform_bar.config(command = self.t_transform_process.yview) #滚动条绑定

        self.lbl_transform_appid.grid(row = 0, column = 0)
        self.ent_transform_appid.grid(row = 0, column = 1, sticky = W + E)
        self.lbl_transform_apikey.grid(row = 1, column = 0)
        self.ent_transform_apikey.grid(row = 1, column = 1, columnspan = 2, sticky = W + E)
        self.lbl_transform_audiopath.grid(row = 2, column = 0)
        self.ent_transform_audiopath.grid(row = 2, column = 1, columnspan = 2, sticky = W + E)
        self.btn_transform_audiobrowse.grid(row = 2, column = 3, sticky = W)
        self.btn_transform_OK.grid(row = 3, column = 1, columnspan = 2)
        self.btn_transform_clear.grid(row = 3, column = 3, sticky = E)
        self.lfrm_transform_process.grid(row = 4, column = 0, columnspan = 4)
        self.t_transform_process.grid(row =0, column = 0)
        self.sb_transform_bar.grid(row = 0, column = 1, sticky = E + N + S) #滚动条放置

        self.topwin.add(self.frm_transform, text = "语音转写")

        #检索版块
        self.frm_search = Frame(self.topwin)

        self.lbl_search_keywords = Label(self.frm_search, text="待检索关键词")
        self.ent_search_keywords = Entry(self.frm_search, textvariable = self.v_search_keywords)
        self.lbl_search_folder = Label(self.frm_search, text="待检索文件夹")
        self.ent_search_folder = Entry(self.frm_search, textvariable = self.v_search_folder)
        self.btn_search_folderbrowse = Button(self.frm_search, text = "浏览", command = self.search_folderbrowse_callback)
        self.btn_search_OK = Button(self.frm_search, text = "开始", command = self.search_OK_callback)
        self.btn_search_clear = Button(self.frm_search, text = "清屏", command = self.search_clear_callback)
        self.lfrm_search_process = LabelFrame(self.frm_search, text = "检索结果")
        self.t_search_process = Text(self.lfrm_search_process, state="disabled")
        self.sb_search_bar = Scrollbar(self.lfrm_search_process) #滚动条创建
        self.t_search_process["yscrollcommand"] = self.sb_search_bar.set #滚动条绑定
        self.sb_search_bar.config(command = self.t_search_process.yview) #滚动条绑定

        self.lbl_search_keywords.grid(row = 0, column = 0)
        self.ent_search_keywords.grid(row = 0, column = 1, columnspan = 2, sticky = W + E)
        self.lbl_search_folder.grid(row = 1, column = 0)
        self.ent_search_folder.grid(row = 1, column = 1, columnspan = 2, sticky = W + E)
        self.btn_search_folderbrowse.grid(row = 1, column = 3, sticky = W)
        self.btn_search_OK.grid(row = 2, column = 1, columnspan = 2)
        self.btn_search_clear.grid(row = 2, column = 3, sticky = E)
        self.lfrm_search_process.grid(row = 3 , column = 0, columnspan = 4)
        self.t_search_process.grid(row = 0, column = 0)
        self.sb_search_bar.grid(row = 0, column = 1, sticky = E + N + S) #滚动条放置

        self.topwin.add(self.frm_search, text = "视频检索")

if __name__ == "__main__":
    root = Tk()
    Application_ui(root).mainloop()
