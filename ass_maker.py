#coding:utf-8
import os
import time
import re




#生成字幕文件，传入参数：
#filename：文件名
#info：文件信息，用于左下角显示用的
#path：文件路径
#ass：最原始的歌词数据
def make_ass(filename, info, path, ass = ''):
    ass = lrc_to_ass(ass)
    file_content = '''[Script Info]
Title: Default ASS file
ScriptType: v4.00+
WrapStyle: 2
Collisions: Normal
PlayResX: 960
PlayResY: 720
ScaledBorderAndShadow: yes
Video Zoom Percent: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: left_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,1,10,10,5,1
Style: right_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,3,10,10,5,1
Style: left_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,7,10,10,5,1
Style: right_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,9,10,10,5,1
Style: center_up,微软雅黑,15,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,8,10,10,5,1
Style: center_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: center_down_big,微软雅黑,25,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 2,0:00:00.00,07:00:00.00,left_down,,0,0,0,,'''+info+'''
Dialogue: 2,0:00:00.00,07:00:00.00,right_down,,0,0,0,,基于树莓派3B\\N已开源，源码见https://biu.ee/pi-live\\N'''+'点播日期：'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'''
Dialogue: 2,0:00:00.00,07:00:00.00,left_up,,0,0,0,,晨旭的树莓派点播台~
Dialogue: 2,0:00:00.00,07:00:00.00,right_up,,0,0,0,,弹幕点播方法请看直播间简介哦~
Dialogue: 2,0:00:00.00,07:00:00.00,right_up,,0,0,0,,测试点播台，功能不断完善中
'''+ass
    file = open(path+'/downloads/'+str(filename)+'.ass','w')    #保存ass字幕文件
    file.write(file_content)
    file.close()

#生成info文件
def make_info(filename, info, path):
    file_content = info
    file = open(path+'/downloads/'+str(filename)+'.info','w')
    file.write(file_content)
    file.close()


#滚动歌词生成
def lrc_to_ass(lrc):
    lrc=lrc.splitlines() #按行分割开来
    list1=['00','00']
    list2=['00','00']
    list3=['00','00']
    list4=[' ',' ']
    result='\r\n'
    for i in lrc:
        matchObj = re.match( r'.*\[(\d+):(\d+)\.(\d+)\]([^\[\]]*)', i)  #正则匹配获取每行的参数，看不懂的去自行学习正则表达式
        if matchObj:    #如果匹配到了东西
            list1.append(matchObj.group(1))
            list2.append(matchObj.group(2))
            list3.append(matchObj.group(3))
            list4.append(matchObj.group(4))
    list1.append('05')
    list1.append('05')
    list2.append('00')
    list2.append('00')
    list3.append('00')
    list3.append('00')
    list4.append(' ')
    list4.append(' ')
    for i in range(2, len(list1)-3):
        text=list4[i-2]+'\\N'+list4[i-1]+'\\N'+list4[i]+'\\N'+list4[i+1]+'\\N'+list4[i+2]
        result+='Dialogue: 2,0:'+list1[i]+':'+list2[i]+'.'+list3[i][0:2]+',0:'+list1[i+1]+':'+list2[i+1]+'.'+list3[i+1][0:2]+',center_down_big,,0,0,0,,'+text+'\r\n'
    return result


