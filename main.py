import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, ttk
import csv
import pandas as pd
import numpy as np
import pickle
import os, shutil
from os import path as PATH
import pathlib, ntpath
import io
import requests
import threading
from time import sleep
import time


path = ""
home = tkinter.Tk()
home.resizable(False, False)


s = Style()
s.configure('1.TFrame', background='white')

s2 = Style()
s2.configure('2.TFrame', background='blue')

s3 = Style()
s3.configure('3.TFrame', background='green')

home.geometry("700x300")
home.title("Earth like planets detector")

frame1 = Frame(home, style="2.TFrame")
frame1.place(height=100, width=150, x=0, y=0)
redbutton = Button(frame1, text="Upload .CSV Here", command=lambda: menuClick(1))
redbutton.pack(ipady=38, ipadx=100)

frame2 = Frame(home)
frame2.place(height=100, width=150, x=0, y=100)
redbutton2 = Button(frame2, text="Nasa Live\nSatalight Data", command=lambda: menuClick(2))
redbutton2.pack(ipady=38, ipadx=100)

frame3 = Frame(home)
frame3.place(height=100, width=150, x=0, y=200)
redbutton3 = Button(frame3, text="Upload/Rest Model", command=lambda: menuClick(3))
redbutton3.pack(ipady=38, ipadx=100)


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


def uploadbttn():
    clear_frame(outputFrame)
    frame_Upload_CSV.filename = filedialog.askopenfilename(initialdir="c:", title="Select csv file")
    path = frame_Upload_CSV.filename
    raw = pd.read_csv(path)
    Status_Update = Text(outputFrame, wrap=NONE)
    Status_Update.pack()
    Status_Update.insert(END, "File data fetched successfully....")
    Model_Name = checkMN()
    filename = Model_Name
    Status_Update.insert(END, "\nChecking Model Status...")
    loaded_model = pickle.load(open(filename, 'rb'))
    Status_Update.insert(END, "\nModel Loaded Successfully...!")
    raw.to_csv('temp.csv')
    Status_Update.insert(END, "\nTemp File Created Sucessfully ... /")
    temp = pd.read_csv('temp.csv')
    Status_Update.insert(END, "\nTemp File Loaded....")
    Tempcloumns = ['default_flag', 'sy_snum', 'sy_pnum', 'disc_year',
                   'pl_controv_flag', 'pl_orbper', 'pl_orbpererr1', 'pl_orbpererr2',
                   'pl_orbperlim', 'pl_orbsmaxlim', 'pl_rade', 'pl_radeerr1',
                   'pl_radeerr2', 'pl_radelim', 'ttv_flag', 'st_teff', 'st_tefferr1',
                   'st_tefferr2', 'st_tefflim', 'st_rad', 'st_raderr1', 'st_raderr2',
                   'st_radlim', 'st_mass', 'st_masserr1', 'st_masserr2', 'st_masslim',
                   'st_met', 'st_meterr1', 'st_meterr2', 'st_metlim', 'st_logg',
                   'st_loggerr1', 'st_loggerr2', 'st_logglim', 'ra', 'dec', 'sy_dist',
                   'sy_disterr1', 'sy_disterr2', 'sy_vmag', 'sy_vmagerr1', 'sy_vmagerr2',
                   'sy_kmag', 'sy_kmagerr1', 'sy_kmagerr2', 'sy_gaiamag', 'sy_gaiamagerr1',
                   'sy_gaiamagerr2']
    remove_col = []
    countrc = 0
    data_insuff = []
    #not_eff = pd.DataFrame()
    l = []
    for x in range(temp.shape[0]):
        for tc in range(len(Tempcloumns)):
            if "True" in str(temp[[Tempcloumns[tc]]].iloc[x:x + 1].isnull()):
                print("yes", Tempcloumns[tc], x)
                # not_eff.append(Live_csv.iloc[[x]])
                l.append(raw.iloc[[x]])
                #data_insuff.append("Data Insufficiant")
                remove_col.append(x)
                break
    countrc = len(l)
    for ind in reversed(range(countrc)):
        print(ind, " ", remove_col[ind])
        # temp=temp.drop(temp.iloc[remove_col[ind]].name)
        # Live_csv=Live_csv.drop(Live_csv.iloc[remove_col[ind]].name)
        temp = temp.drop(remove_col[ind])
        raw=raw.drop(remove_col[ind])
    #for tc in range(len(Tempcloumns)):
    #   arrynull = temp[Tempcloumns[tc]].isnull()
    #    for x in range(temp.shape[0]):
    #        if arrynull[x] == True:
    #            not_eff = raw.iloc[x:x + 1]
    #            data_insuff = "Data Insufficiant"
    #            remove_col.append(x)
    #            countrc += 1
    #for ind in range(countrc):
        #temp = temp.drop(temp.iloc[remove_col[ind]].name)
        #raw = raw.drop(raw.iloc[remove_col[ind]].name)
     #pass

    for i in temp.columns:
        if i in Tempcloumns:
            pass
        else:
            temp = temp.drop([i], axis=1)

    logcol = ['st_teff', 'pl_rade', 'pl_orbper']
    for i in temp.columns:
        if i in logcol:
            temp[i] = (temp[i] + 1).transform(np.log)
    Status_Update.insert(END, "\nData Prepared for Feeding Process ...")
    y_predr = loaded_model.predict(temp)
    Habitabilty = []
    Status_Update.insert(END, "\nModel Output Created ..../")
    for i in y_predr:
        if i == 0:
            Habitabilty.append("False")
        if i == 1:
            Habitabilty.append("True")



    #raw=raw.append(not_eff)
    for i in range(len(l)):
        raw = raw.append(l[i])
        Habitabilty.append("Data Insufficiant")
        print("appending")
    print(Habitabilty)
    Status_Update.insert(END, "\nWorking on OutputFile..../")
    raw['Habitabilty'] = Habitabilty
    raw=raw.sort_index()
    raw.to_csv('output.csv')
    #temp.to_csv('output.csv')
    Status_Update.insert(END, "\nOutput File Created ... .!")
    os.remove("temp.csv")
    Status_Update.insert(END, "\nTemp File Deleted Sucessfuly.. . .|")
    Status_Update.insert(END, "\nSucess 1  Error0 !")


def output():
    clear_frame(outputFrame)
    pd.set_option("display.max_rows", 7)
    output = pd.read_csv('output.csv', index_col=[0])
    h = Scrollbar(outputFrame, orient='horizontal')
    v = Scrollbar(outputFrame, orient='vertical')
    t = Text(outputFrame, wrap=NONE, xscrollcommand=h.set,
             yscrollcommand=v.set)
    # lb=Label(outputFrame, text=output, background="white")
    # lb.pack()
    h.pack(side=BOTTOM, fill=X)

    v.pack(side=RIGHT, fill=Y)

    # with open('output.csv', 'r')as csv_file:
    # csv_read = csv.reader(csv_file)
    # for line in csv_read:
    t.insert(END, output)
    h.config(command=t.xview)
    v.config(command=t.yview)
    t.pack()


def fullR():
    Fullresult = Toplevel(height=600, width=1000)
    Fullresult.resizable(False, False)
    frame_Result_show = Frame(Fullresult)
    frame_Result_show.place(x=20, y=20, height=580, width=980)
    hFR = Scrollbar(frame_Result_show, orient='horizontal')
    vFR = Scrollbar(frame_Result_show, orient='vertical')
    hFR.pack(side=BOTTOM, fill=X)
    vFR.pack(side=RIGHT, fill=Y)
    ResultTextbox = Text(frame_Result_show, wrap=NONE, xscrollcommand=hFR.set,
             yscrollcommand=vFR.set,height=580, width=980)
    csv_read = pd.read_csv('output.csv', chunksize=1, index_col=[0])
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    pd.set_option('display.width', None)
    ResultTextbox.insert(END, csv_read.read())
    ResultTextbox.pack()
    hFR.config(command=ResultTextbox.xview)
    vFR.config(command=ResultTextbox.yview)

frame_Upload_CSV = Frame(home)
frame_Upload_CSV.place(height=300, width=550, x=150, y=0)
uploadbutton = Button(frame_Upload_CSV, text="Select File", command=uploadbttn)
File_Lable=StringVar()
filestatus = Label(frame_Upload_CSV, text="File not detected....").place(x=140, y=55)
Resultbutton = Button(frame_Upload_CSV, text="Fetch Result", command=output)
uploadbutton.place(x=50, y=50)
Resultbutton.place(x=50, y=90)
outputFrame = Frame(frame_Upload_CSV, style="1.TFrame")
outputFrame.place(height=120, width=520, x=20, y=125)

"""
my_canvas=Canvas(outputFrame)
my_canvas.pack(side=BOTTOM,fill=BOTH,expand=1)
myscrollbar= ttk.Scrollbar(outputFrame,orient=HORIZONTAL,command=my_canvas.xview)
myscrollbar.pack(side=BOTTOM, fill=X)
my_canvas.configure(xscrollcommand=myscrollbar.set)
my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
outputchildFrame=Frame(my_canvas,style="1.TFrame")
my_canvas.create_window((0,0),window=outputchildFrame,anchor="sw")

"""



ShowfullR = Button(frame_Upload_CSV, text="Show Full Result", command=fullR)
ShowfullR.place(x=400, y=255)

frame_Nasa_Live = Frame(home)


start_data_point=0
end_data_point=10
ok=0
ThreadLock=threading.Lock()



def fullL():
        ThreadLock.acquire()
        Fullresult_Live = Toplevel(height=600, width=1000)
        Fullresult_Live.resizable(False, False)
        frame_Result_show_Live = Frame(Fullresult_Live)
        frame_Result_show_Live.place(x=20, y=20, height=580, width=980)

        hFR = Scrollbar(frame_Result_show_Live, orient='horizontal')
        vFR = Scrollbar(frame_Result_show_Live, orient='vertical')
        hFR.pack(side=BOTTOM, fill=X)
        vFR.pack(side=RIGHT, fill=Y)
        ResultTextbox = Text(frame_Result_show_Live, wrap=NONE, xscrollcommand=hFR.set,
                             yscrollcommand=vFR.set, height=580, width=980)
        csv_read = pd.read_csv('liveoutput.csv', chunksize=1, index_col=[0])
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        pd.set_option('display.width', None)
        ResultTextbox.insert(END, csv_read.read())
        ResultTextbox.pack()
        hFR.config(command=ResultTextbox.xview)
        vFR.config(command=ResultTextbox.yview)
        ThreadLock.release()
        time.sleep(5)






def outputND():
    clear_frame(Nasa_data_Frame)
    Status_Update = Text(Nasa_data_Frame, wrap=NONE)
    Status_Update.pack()
    Status_Update.insert(END, "Fetching Url..../")
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+from+ps+order+by+releasedate+desc&format=csv"
    fecthed_data= requests.get(url).content
    Status_Update.insert(END, "\nLive Data Raw Fetched...")
    Live_csv_temp= pd.read_csv(io.StringIO(fecthed_data.decode('utf-8')), index_col=[0])
    Live_csv_temp.to_csv('live_temp.csv')
    global countround
    countround=Live_csv_temp.shape[0]
    Status_Update.insert(END, "\nLive Raw File Saved....")
    #Live_data_update(Status_Update)

    t1= threading.Thread(target=Live_data_update, args=(Status_Update,countround,))

    #t2= threading.Thread(target=fullL)

    t1.start()
    #t1.join()

def Live_data_update(Status_Update,countround):
  for thrd in range(countround):
    Status_Update.insert(END, "\nGetting Live Data From Website..../")
    Live_csv= pd.read_csv('live_temp.csv', index_col=[0])
    global start_data_point ,end_data_point
    k=Live_csv.iloc[start_data_point:end_data_point]
    start_data_point+=11
    end_data_point+=11
    k = k.to_string()
    k = "'" + k[36:-1] + "'"
    k = k.replace(", ", "\',\'")
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+distinct+*+from+ps+where+pl_name+IN+(" + k + ")+order+by+releasedate+desc&format=csv"
    s = requests.get(url).content
    Status_Update.insert(END, "\nLive Data Fetched Sucessfully!..../")
    Live_csv= pd.read_csv(io.StringIO(s.decode('utf-8')), index_col=[0])
    #global current_Live_object
    #current_Live_object=current_Live_object+Live_csv.shape[0]
    Live_csv.to_csv('temp.csv')
    Live_csv = pd.read_csv('temp.csv')
    temp = pd.read_csv('temp.csv')
    Status_Update.insert(END, "\nLoadding Machine Learning Model..../")
    Model_Name = checkMN()
    filename = Model_Name
    loaded_model = pickle.load(open(filename, 'rb'))
    temp = pd.read_csv('temp.csv')
    Tempcloumns = ['default_flag', 'sy_snum', 'sy_pnum', 'disc_year',
                   'pl_controv_flag', 'pl_orbper', 'pl_orbpererr1', 'pl_orbpererr2',
                   'pl_orbperlim', 'pl_orbsmaxlim', 'pl_rade', 'pl_radeerr1',
                   'pl_radeerr2', 'pl_radelim', 'ttv_flag', 'st_teff', 'st_tefferr1',
                   'st_tefferr2', 'st_tefflim', 'st_rad', 'st_raderr1', 'st_raderr2',
                   'st_radlim', 'st_mass', 'st_masserr1', 'st_masserr2', 'st_masslim',
                   'st_met', 'st_meterr1', 'st_meterr2', 'st_metlim', 'st_logg',
                   'st_loggerr1', 'st_loggerr2', 'st_logglim', 'ra', 'dec', 'sy_dist',
                   'sy_disterr1', 'sy_disterr2', 'sy_vmag', 'sy_vmagerr1', 'sy_vmagerr2',
                   'sy_kmag', 'sy_kmagerr1', 'sy_kmagerr2', 'sy_gaiamag', 'sy_gaiamagerr1',
                   'sy_gaiamagerr2']
    remove_col = []
    countrc = 0
    data_insuff = []
    Status_Update.insert(END, "\nPreparing Live Data For Prediction..../")
    l = []
    for x in range(temp.shape[0]):
        for tc in range(len(Tempcloumns)):
            if "True" in str(temp[[Tempcloumns[tc]]].iloc[x:x + 1].isnull()):
                l.append(Live_csv.iloc[[x]])
                remove_col.append(x)
                break
    countrc = len(l)

    for ind in reversed(range(countrc)):
        temp = temp.drop(remove_col[ind])
        Live_csv = Live_csv.drop(remove_col[ind])

    for i in temp.columns:
        if i in Tempcloumns:
            pass
        else:
            temp = temp.drop([i], axis=1)

    logcol = ['st_teff', 'pl_rade', 'pl_orbper']

    for i in temp.columns:
        if i in logcol:
            temp[i] = (temp[i] + 1).transform(np.log)
    y_predr = loaded_model.predict(temp)
    Status_Update.insert(END, "\nResult Predicted....!")
    Habitabilty = []
    for i in y_predr:
        if i == 0:
            Habitabilty.append("False")
        if i == 1:
            Habitabilty.append("True")

    for i in range(len(l)):
        Live_csv= Live_csv.append(l[i])
        Habitabilty.append("Data Insufficiant")
    Status_Update.insert(END, "\nResult Loaded....!")
    Live_csv['Habitabilty'] = Habitabilty
    Live_csv = Live_csv.sort_index()
    if thrd == 0:
        Live_csv.to_csv('liveoutput.csv')
    else:
        tliop=pd.read_csv("liveoutput.csv",index_col=[0])
        newid=tliop.shape[0]
        Live_csv.index=Live_csv.index+newid
        tliop=tliop.append(Live_csv)
        tliop.to_csv('liveoutput.csv')

    os.remove("temp.csv")
    if end_data_point >= countround:
        break
    #if thrd == 2:
    #   break
    #print(thrd)

Nasa_data_Frame = Frame(frame_Nasa_Live, style="1.TFrame")
Nasa_data_Frame.place(height=200, width=520, x=20, y=50)
ShowfulllL = Button(frame_Nasa_Live, text="Show Full Result", command=fullL)
ShowfulllL.place(x=400, y=255)
ResultNDbutton = Button(frame_Nasa_Live, text="Fetch Result", command=outputND)
ResultNDbutton.place(x=20, y=20)

frame_Model = Frame(home)
Model_Name = ""
Lable_Model = StringVar()


def UploadM():
    Custom_Upload = filedialog.askopenfilename(initialdir="c:", title="Select Model file")
    DestinationFolder = pathlib.Path().absolute()
    shutil.copy(Custom_Upload, DestinationFolder)
    Model_Name = ntpath.basename(Custom_Upload)
    Lable_Model.set("Current Live Model:" + Model_Name)
    CMN_file = open("Current_Model_Name.txt", 'w')
    CMN_file.write(Model_Name)
    CMN_file.close()


def ResetM():
    Model_Name = "DefultModel.sav"
    CMN_file = open("Current_Model_Name.txt", 'w')
    CMN_file.write(Model_Name)
    CMN_file.close()
    Lable_Model.set("Current Live Model:" + Model_Name)


def checkMN():
    if (PATH.isfile("Current_Model_Name.txt")):
        CMN_file = open("Current_Model_Name.txt", 'r')
        Model_Name = CMN_file.read()
        return Model_Name
    else:
        Model_Name = "DefultModel.sav"
        CMN_file = open("Current_Model_Name.txt", 'w')
        CMN_file.write(Model_Name)
        CMN_file.close()
        return Model_Name


Model_Name = checkMN()
Lable_Model.set("Current Live Model:" + Model_Name)
Current_Model_Name = Label(frame_Model, textvariable=Lable_Model).place(x=140, y=55)
Upload_custom_model = Button(frame_Model, text="Upload Custom Model", command=UploadM)
Upload_custom_model.place(x=190, y=100)
Reset_Defult_model = Button(frame_Model, text="Reset Defult Model", command=ResetM)
Reset_Defult_model.place(x=200, y=200)


def menuClick(args):
    if args == 1:
        frame_Nasa_Live.place_forget()
        frame_Model.place_forget()
        frame_Upload_CSV.place(height=300, width=550, x=150, y=0)
    if args == 2:
        frame_Upload_CSV.place_forget()
        frame_Model.place_forget()
        frame_Nasa_Live.place(height=300, width=550, x=150, y=0)
    if args == 3:
        frame_Upload_CSV.place_forget()
        frame_Nasa_Live.place_forget()
        frame_Model.place(height=300, width=550, x=150, y=0)
        top = Toplevel()

        Label(top,
              text="Don't do any changes in this module if you are not professional!\n It will take direct effect on result of the software ").pack()


home.mainloop()
