import tkinter
from tkinter import Toplevel, filedialog
import os
import shutil
import frame_divide
import frame_merge
import highlight

#cutsin 변수
start_dir = "./CutSin/Start.mp4"
cut_dir = "./CutSin/Sin.mp4"
finish_dir = "./CutSin/Finish.mp4"

window=tkinter.Tk()

#UI초기값
window.title("Short Track Highlight Editior")
window.geometry("792x440")
window.resizable(False, False)
image = tkinter.PhotoImage(file='startUI.png')

#문구 설정
label=tkinter.Label(window, image=image)
# label=tkinter.Label(window, width=30, height=28, fg="white", relief="solid")

label.pack()

#버튼 클릭시
def opendir():
   root = tkinter.Toplevel()#toplevel은 새창
   root.withdraw()
   #동영상이 있는 폴더 실행
   #폴더가 아닌 파일을 하고 싶은 경우 filedialog.askopenfilename()
   video_path = filedialog.askopenfilename(parent=root,initialdir='./ShortTrack',title='Please select a video')
   #fame_divide로 동영상 파일 넘긴뒤 실행
   count,imagePath = frame_divide.frame_divide(video_path)
   print("Finish divide")
   
   

   #하이라이트 실행
   total_score=highlight.highlight(count,video_path)
   print("\nTotal score",total_score)
   #merge실행
   frame_merge.frame_merge(video_path,total_score,start_dir,cut_dir,finish_dir)

   #폴더 열기
   path_finish="./outputVideo"#결과창
   path = os.path.realpath(path_finish)
   os.startfile(path)
#종료시
def on_closing(n,num):
   #캐쉬파일 삭제
   if(num == 1):
      if os.path.exists("./__pycache__"):
         shutil.rmtree("./__pycache__")
   n.destroy()

def open_cutsin_video(n):
   root = tkinter.Toplevel()#toplevel은 새창
   root.withdraw()
   if(n==1):
      global start_dir
      start_dir = filedialog.askopenfilename(parent=root,initialdir='./ShortTrack',title='Please select a Start video')
   if(n==2):
      global cut_dir
      cut_dir = filedialog.askopenfilename(parent=root,initialdir='./ShortTrack',title='Please select a Cut video')
   if(n==3):
      global finish_dir
      finish_dir = filedialog.askopenfilename(parent=root,initialdir='./ShortTrack',title='Please select a Finish video')

def open_cutsin():
   window_cutsin = tkinter.Toplevel()
   window_cutsin.geometry("792x440")
   window_cutsin.resizable(False, False)
   image = tkinter.PhotoImage(file='startUI2.png')

   label_cutsin=tkinter.Label(window_cutsin, image=image)
   label_cutsin.pack()

   button_Start = tkinter.Button(window_cutsin, text="Start", background="white", borderwidth=0,  padx=0, pady=0, width=15, command=lambda : open_cutsin_video(1), repeatdelay=1000, repeatinterval=100)
   button_Start.place(x=510, y=90)

   button_Cut = tkinter.Button(window_cutsin, text="Cut", background="white", borderwidth=0,  padx=0, pady=0, width=15, command=lambda : open_cutsin_video(2), repeatdelay=1000, repeatinterval=100)
   button_Cut.place(x=510, y=180)

   button_Finish = tkinter.Button(window_cutsin, text="Finish", background="white", borderwidth=0,  padx=0, pady=0, width=15, command=lambda : open_cutsin_video(3), repeatdelay=1000, repeatinterval=100)
   button_Finish.place(x=510, y=270)

   button_Cutsin_close = tkinter.Button(window_cutsin, text="Close", background="white", borderwidth=0,  padx=0, pady=0, width=15, command=lambda : on_closing(window_cutsin,2), repeatdelay=1000, repeatinterval=100)
   button_Cutsin_close.place(x=510, y=360)
  
   window_cutsin.mainloop()
   
#버튼 설정
button = tkinter.Button(window, text="Select Video", background="white", borderwidth=0,  padx=0, pady=0, width=15, command=opendir, repeatdelay=1000, repeatinterval=100)
button.place(x=510, y=150)

button_Cutsin = tkinter.Button(window, text="Cut Scene", background="white", borderwidth=0, padx=0, pady=0, width=15, command=open_cutsin, repeatdelay=1000, repeatinterval=100)
button_Cutsin.place(x=510, y=300)

#닫기버튼
window.protocol("WM_DELETE_WINDOW", lambda : on_closing(window,1))


window.mainloop()