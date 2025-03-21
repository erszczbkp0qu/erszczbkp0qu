#coding:utf-8
import os
import sys
import time
import random
from mutagen.mp3 import MP3
import var_set
import shutil
import _thread

path = var_set.path
rtmp = var_set.rtmp
live_code = var_set.live_code

def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

def remove_v(filename):
    try:
        shutil.move(path+'/downloads/'+filename,path+'/default_mp3/')
    except Exception as e:
        print(e)
    try:
        os.remove(path+'/downloads/'+filename.replace(".flv",'')+'ok.ass')
        os.remove(path+'/downloads/'+filename.replace(".flv",'')+'ok.info')
    except Exception as e:
        print(e)
        print('delete error')

while True:
    try:
        files = os.listdir(path+'/downloads')
        files.sort()
        count=0
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)):
                audio = MP3(path+'/downloads/'+f)
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                if(seconds > 600):
                    print('too long,delete')
                else:
                    pic_files = os.listdir(path+'/default_pic')
                    pic_files.sort()
                    pic_ran = random.randint(0,len(pic_files)-1)
                    print('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                try:
                    os.remove(path+'/downloads/'+f)
                    os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.ass')
                    os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.info')
                except:
                    print('delete error')
                count+=1
            if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):
                print('flv:'+f)
                print('ffmpeg -re -i "'+path+"/downloads/"+f+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -i "'+path+"/downloads/"+f+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.rename(path+'/downloads/'+f,path+'/downloads/'+f.replace("ok",""))
                _thread.start_new_thread(remove_v, (f.replace("ok",""),))
                count+=1
        if(count == 0):
            print('no media')
            mp3_files = os.listdir(path+'/default_mp3')
            mp3_files.sort()
            mp3_ran = random.randint(0,len(mp3_files)-1)
            
            if(mp3_files[mp3_ran].find('.mp3') != -1):
                pic_files = os.listdir(path+'/default_pic')
                pic_files.sort()
                pic_ran = random.randint(0,len(pic_files)-1)
                audio = MP3(path+'/default_mp3/'+mp3_files[mp3_ran])
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                print('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
            if(mp3_files[mp3_ran].find('.flv') != -1):
                print('ffmpeg -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
    except Exception as e:
        print(e)

        