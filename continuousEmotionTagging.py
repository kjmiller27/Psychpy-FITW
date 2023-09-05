        #Continuous Emotion Tagging
#Sophie Wohltjen (06/2022) iterating on work done by Emma Templeton (12/2016)

#TASK: Displays instructions to participants, gives them a chance to practice tagging
#changes in their emotional state, then plays conversation video. Participants press the space bar 
# to stop the video and tag their emotion shifts, as well as continuously move the mouse to tag
#how intensely they were feeling that emotion. Script queries and records mouse 
#position every 0.1 seconds. 

#########################################
#import stuff
from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os
import sys
import numpy as np
import pandas as pd
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle,choice
import psychopy.core

import time

#########################################

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

#input subject and partner ID; store values for later
gui=psychopy.gui.Dlg() 
gui.addField("Dyad ID: ")
gui.addField("Subject ID: ")
gui.addField("Partner ID: ")
gui.addField("Subject Initials: ")
gui.show()
dyad = gui.data[0]
subID=gui.data[1]
partnerID=gui.data[2]
subinitials=gui.data[3]

# Open output file and write header
output_name = './subject_ratings/'+str(subID)+'_'+str(partnerID)+'_'+str(subinitials)+'rating.csv'
if os.path.exists(output_name): #if path exists, remame it to avoid overwriting data
    newSubID = subID+"000"
    output_name = './subject_ratings/'+str(newSubID)+'_'+str(partnerID)+'_'+str(subinitials)+'rating.csv'
output_csv = open(output_name, 'w')
output_csv.write('SubID,PartnerID,Rating,EmoRating,Time,Movietime,Shift,Description\n')

#########################################
#SETUP: DEFINE WINDOW

#Window
win=psychopy.visual.Window(size=[1280, 800], units="pix", fullscr=True, color=[-1, -1, -1], winType='pyglet')

#Define screen center
cX=0
cY=0

videoX=cX
videoY=cY+50
#########################################
#DRAW SCALE

mouse = psychopy.event.Mouse(visible=False,newPos=[0,-200], win=win)

## COPY THIS CODE TO MAKE NEW RATING SCALE - CHANGE VARIABLE NAME
#Draw Rating scale
scaleX=cX
scaleY=cY-200
ratingScaleWidth=480
ratingScaleHeight=10
ratingScale = psychopy.visual.Rect(win, width=ratingScaleWidth, height=ratingScaleHeight, pos=[scaleX,scaleY], color='white')

sliderLeftEnd = -240
sliderRightEnd = 240

scaleX=cX
scaleY=cY-200
ratingScaleEmoWidth=480
ratingScaleEmoHeight=10
ratingScaleEmo = psychopy.visual.Rect(win, width=ratingScaleEmoWidth, height=ratingScaleEmoHeight, pos=[scaleX,scaleY], color='white')

sliderLeftEnd = -240
sliderRightEnd = 240

#Draw Slider Handle 
handleWidth=1
handleHeight=20
handle = psychopy.visual.Rect(win, width=handleWidth, height=handleHeight, pos=[scaleX,scaleY], color='blue')

handleEmoWidth=1
handleEmoHeight=20
handleEmo = psychopy.visual.Rect(win, width=handleWidth, height=handleHeight, pos=[scaleX,scaleY], color='blue')

#Draw Labels
label1X=-240
label1Y=scaleY-25
label1_txt="Not at all"
label1=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center',text=label1_txt, color=[1, 1, 1], height=20, pos=[label1X,label1Y])

label2X=240
label2_txt="Very"
label2=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=label2_txt, color=[1, 1, 1], height=20, pos=[label2X,label1Y])

#Draw Title
title_txt="How connected were you feeling to your partner at this moment?"
titleY=videoY+225
title=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=title_txt, color=[1, 1, 1], height=25, pos=[cX,titleY], wrapWidth=550)

#Draw reminder
#remind_txt="**Remember to press tab when your feelings in the video change!"
#remind=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=remind_txt, color=[1, 1, 1], height=15, pos=[0,-300], wrapWidth=250)

#Draw instructions for getting back to the video
#Draw reminder
hint_txt="press tab to return to the video."
hint=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=hint_txt, color=[1, 1, 1], height=15, pos=[0,-300], wrapWidth=250)

#Draw free response box
inst_self = "please use the box below to write about how YOU were feelings at this moment."
instext_self = psychopy.visual.TextStim(win=win,alignText='center', anchorHoriz='center',text=inst_self,color=[1, 1, 1],height=25,pos=[cX,titleY],wrapWidth=550)
inst_partner = "please use the box below to write about how YOUR PARTNER was feeling at this moment."
instext_partner = psychopy.visual.TextStim(win=win,alignText='center', anchorHoriz='center',text=inst_partner,color=[1, 1, 1],height=25,pos=[cX,titleY],wrapWidth=550)
textEntry = ""
textbox = psychopy.visual.TextBox2(win=win,text=textEntry,alignment='left',borderColor='white',pos=[cX,titleY-200],letterHeight=25,size=[550,300],editable=True)

#Draw Emotion box Title
title_emo_txt="How emotionally intense were YOU feeling at this moment?"
title_emo_partner_txt="How emotionally intense was YOUR PARTNER feeling at this moment?"
title_emo_Y=videoY-250
title_emo=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=title_emo_txt, color=[1, 1, 1], height=25, pos=[cX,title_emo_Y], wrapWidth=550)
title_emo_partner=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=title_emo_partner_txt, color=[1, 1, 1], height=25, pos=[cX,title_emo_Y], wrapWidth=550)

#########################################
#advance instructions
advance_txt="Press any key to continue"
advance=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=advance_txt, color=[1, 1, 1], height=30, pos=[0,-250], wrapWidth=1000)

##EDIT INSTRUCTION TEXT AND SPACING
#instruction text
instr1="Now you will watch the recorded conversation that you just had. As you watch, think back to how you felt during that conversation."
instr2="Your first task is to continuously move a bar on a response slider using your mouse to indicate how connected you felt to your partner during the conversation." 
instr3="The response slider runs from 'not at all' to 'very'. Move the bar across the slider to indicate changes in how connected you felt."
#instr2="Your first task is to continuously move a bar on a response slider using your mouse to indicate the intensity of your feelings during the conversation (e.g., if you were overcome with emotion, that would signal very intense feelings). The response slider runs from 'not at all' to 'very'. Move the bar across the slider to indicate changes in the intensity of your feelings."
instr4="You will also be prompted at various points to write about how you OR your partner were feeling during a moment of the conversation (e.g. My partner was feeling happy, or I was nervous about how my partner would respond to me)." 
instr5="After you write about how you OR your partner felt, you will then be prompted to indicate the intensity of you OR your partner's feelings (e.g., if you/they were overcome with emotion, that would signal very intense feelings)."
instr6="You will use your mouse to move a response slider, which runs from 'not at all' to 'very'. Move the bar across the slider to indicate the intensity of you OR your partner's feelings."
instr7="These ratings will not be shared with your study partner. Please accurately and continuously report how connected you felt, and please accurately describe how you OR your partner were feeling when prompted."

instruct1=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr1,color=[1, 1, 1],height=30,pos=[-500,300],wrapWidth=1000)
instruct2=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr2,color=[1, 1, 1],height=30,pos=[-500,150],wrapWidth=1000)
instruct3=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr3,color=[1, 1, 1],height=30,pos=[-500,0],wrapWidth=1000)
instruct4=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr4,color=[1, 1, 1],height=30,pos=[-500,300],wrapWidth=1000)
instruct5=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr5,color=[1, 1, 1],height=30,pos=[-500,150],wrapWidth=1000)
instruct6=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr6,color=[1, 1, 1],height=30,pos=[-500,0],wrapWidth=1000)
instruct7=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=instr7,color=[1, 1, 1],height=30,pos=[-500,-150],wrapWidth=1000)

practice_txt = "Before watching the conversation, take some time to practice using the rating scale and writing about your feelings. Move the mouse to move the slider, and use the text box provided to write about your feelings."
practice=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=practice_txt,color=[1, 1, 1],height=30,pos=[-500,250],wrapWidth=1000)

reminder_txt = "Press the space bar once you feel comfortable using the slider and typing in the text box."
reminder=psychopy.visual.TextStim(win=win,alignText='center', anchorHoriz='center',text=reminder_txt,color=[1, 1, 1],height=20,pos=[0,0],wrapWidth=400)

#########################################
#LOAD VIDEOS

#Loading Screen
load="Video is loading. This may take several minutes."
text=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=load, color=[1, 1, 1], height=30, wrapWidth=1000)
text.setAutoDraw(True)
#win.flip()

#Loaded Screen
load="Video has loaded!"
text2=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=load, color=[1, 1, 1], height=30, wrapWidth=1000)

#Define videos
#Videos are named / loaded based on subID and partnerID
videoFile = './subs'+str(subID)+'_'+str(partnerID)+'.mov'
if not os.path.exists(videoFile): #allow flexibility for subID order
    videoFile = './subs'+str(partnerID)+'_'+str(subID)+'.mov'
#videoFile = './videos/test.mov' #to test script with smaller video
practiceVideo = './test.mov'

#Load Conversation Video
mov = visual.MovieStim3(win, videoFile, size=(640, 360),
    flipVert=False, flipHoriz=False, pos=[videoX,videoY], loop=False)

#Load Practice Video
movPractice = visual.MovieStim3(win, practiceVideo, size=(640, 360),
    flipVert=False, flipHoriz=False, pos=[videoX,videoY], loop=False)

#Alert experimeter that the videos have been loaded
if mov.duration > 0:
    text.setAutoDraw(False)
    text2.draw()
    win.flip()
    psychopy.event.waitKeys(keyList=['space'])

#Create random intervals to probe about emotions
exp_samp_practice = 22
probe_timings = pd.read_csv('./probe_timings/D{0}_timings.csv'.format(dyad))
exp_samp = probe_timings['times'].tolist()
whichperson = probe_timings['subject'].tolist()
print(whichperson)


#########################################
#INSTRUCTIONS
instruct1.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct1.draw()
instruct2.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct1.draw()
instruct2.draw()
instruct3.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct4.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct4.draw()
instruct5.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct4.draw()
instruct5.draw()
instruct6.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct4.draw()
instruct5.draw()
instruct6.draw()
instruct7.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

#########################################
#PRACTICE TRIALS 
practice.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

#########################################
#PRACTICE TRIALS 
movtime = core.Clock()
movPractice.setAutoDraw(True)
ratingScale.setAutoDraw(True)
ratingScaleEmo.setAutoDraw(True)
handle.setAutoDraw(True)
label1.setAutoDraw(True)
label2.setAutoDraw(True)
title.setAutoDraw(True)
psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text="debug",color=[1, 1, 1],height=30,pos=[-500,-150],wrapWidth=1000).draw()
win.flip()
psychopy.event.waitKeys()
#remind.setAutoDraw(True)x

oldMouseX = 0

#play practice video
while movPractice.status != visual.FINISHED:
    
    mouseRel=mouse.getRel()
    mouseX=oldMouseX + mouseRel[0]
    if mouseX > 240:
        mouseX = 240
    if mouseX < -240:
        mouseX = -240
    handle.setPos([mouseX, scaleY])
    #handle.draw()
    oldMouseX=mouseX
    
    win.flip()

    if event.getKeys(['escape']):
        #everything before "break" is just to give participants something
        #to look at during the weird lag
        win.flip()

        ratingScale.setAutoDraw(False)
        handle.setAutoDraw(False)
        label1.setAutoDraw(False)
        label2.setAutoDraw(False)
        title.setAutoDraw(False)
        movPractice.setAutoDraw(False)
        fillerTxt="Responses are being recorded"
        filler=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=fillerTxt, color=[1, 1, 1], height=30, wrapWidth=1000)
        filler.draw()
        break
    if round(movtime.getTime()) == exp_samp_practice:
        pausetime = core.Clock()
        if movPractice.status == PLAYING:
            textbox.setAutoDraw(True)
            instext_self.setAutoDraw(True)
            title_emo.setAutoDraw(True)
            hint.setAutoDraw(True)
            title.setAutoDraw(False)
            ratingScale.setAutoDraw(False)
            handle.setAutoDraw(False)
            label1.setAutoDraw(False)
            label2.setAutoDraw(False)
            movPractice.pause()
            movPractice.setAutoDraw(False)
            movPractice.status = PAUSED
    if event.getKeys(['tab']):
        movtime.addTime(-pausetime.getTime())
        movPractice.play()
        movPractice.setAutoDraw(True)
        textbox.setAutoDraw(False)
        title_emo.setAutoDraw(False)
        instext_self.setAutoDraw(False)
        hint.setAutoDraw(False)
        title.setAutoDraw(True)
        ratingScale.setAutoDraw(True)
        handle.setAutoDraw(True)
        label1.setAutoDraw(True)
        label2.setAutoDraw(True)
        textbox.text = ""

#replace practice video with instructions
while movPractice.status == visual.FINISHED:
    reminder.draw()
    title.setAutoDraw(False)
    ratingScale.setAutoDraw(False)
    handle.setAutoDraw(False)
    label1.setAutoDraw(False)
    label2.setAutoDraw(False)
    win.flip()
    
    #mouseRel=mouse.getRel()
    #mouseX=oldMouseX + mouseRel[0]
    #if mouseX > 240:
        #mouseX = 240
    #if mouseX < -240:
        #mouseX = -240
    #handle.setPos([mouseX, scaleY])
    #handle.draw()
    #oldMouseX=mouseX

    if event.getKeys(['space']):
        #everything before "break" is just to give participants something
        #to look at during the weird lag
        win.flip()

        ratingScale.setAutoDraw(False)
        handle.setAutoDraw(False)
        label1.setAutoDraw(False)
        label2.setAutoDraw(False)
        title.setAutoDraw(False)
        fillerTxt="Responses are being recorded"
        filler=psychopy.visual.TextStim(win=win, alignText='center', anchorHoriz='center', text=fillerTxt, color=[1, 1, 1], height=30, wrapWidth=1000)
        filler.draw()
        break

win.flip()

ratingScale.setAutoDraw(False)
handle.setAutoDraw(False)
label1.setAutoDraw(False)
label2.setAutoDraw(False)
title.setAutoDraw(False)
#remind.setAutoDraw(False)

#########################################
#POST-PRACTICE SCREEN

mouse = psychopy.event.Mouse(visible=False, win=win)

practice_txt2 = "Now that you are familiar with the rating scale and writing in the text box, it's time to start the task! Remember to continuously move the slider to accurately report how connected you felt during the conversation, and remember to accurately report how you OR your partner were feeling (e.g. happy, nervous) at that moment in the conversation, when prompted. The video will play immediately after this screen."
practice2=psychopy.visual.TextStim(win=win,alignText='left', anchorHoriz='left',text=practice_txt2,color=[1, 1, 1],height=30,pos=[-500,250],wrapWidth=1000)

practice2.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

#########################################
#INITIALIZE VARIABLES

movtime=core.Clock()
ratingScale.setAutoDraw(True)
handle.setAutoDraw(True)
label1.setAutoDraw(True)
label2.setAutoDraw(True)
title.setAutoDraw(True)
mov.setAutoDraw(True)
#remind.setAutoDraw(True)

timeAtLastRecord = 0
TIME_INTERVAL = 0.1 #how frequently to sample / record scale responses
oldMouseX = 0 #mouse position in x-axis

start_time = time.time()
i = 0

while mov.status != visual.FINISHED:
       
    mouseRel=mouse.getRel()
    mouseX=oldMouseX + mouseRel[0]
    if mouseX > 240:
        mouseX = 240
    if mouseX < -240:
        mouseX = -240
    handle.setPos([mouseX, scaleY])
    #handle.draw()
    oldMouseX=mouseX
           
    cur_time = time.time()
    ##COPY sliderValue line of code to make a new line for the emotion slider
    #query and record rating info every 0.1 seconds
    if (cur_time - start_time) > (0.1 * i) and mov.status == PAUSED:
        i += 1
        sliderValue = round((mouseX - sliderLeftEnd) / (sliderRightEnd - sliderLeftEnd) * 100, 0)
        sliderValueEmo = round((mouseX - sliderLeftEnd) / (sliderRightEnd - sliderLeftEnd) * 100, 0)
        output_time = round(cur_time - start_time, 2)
        shift = 1
        output_str = ','.join([subID, partnerID, str(sliderValue), str(output_time),str(movtime.getTime()),str(shift),textbox.getText()]) + '\n'
        output_csv.write(output_str)
    elif (cur_time - start_time) > (0.1 * i) and mov.status == PLAYING:
        i += 1
        sliderValue = round((mouseX - sliderLeftEnd) / (sliderRightEnd - sliderLeftEnd) * 100, 0)
        sliderValueEmo = round((mouseX - sliderLeftEnd) / (sliderRightEnd - sliderLeftEnd) * 100, 0)
        output_time = round(cur_time - start_time, 2)
        shift = 0
        output_str = ','.join([subID, partnerID, str(sliderValue), str(output_time),str(movtime.getTime()),str(shift),'']) + '\n'
        output_csv.write(output_str)
     
    win.flip() 
    if event.getKeys(['escape']):
        break
        
    if (round(movtime.getTime()) in exp_samp):
        pausetime = core.Clock()
        ind = exp_samp.index(round(movtime.getTime()))
        if mov.status == PLAYING:
            textbox.setAutoDraw(True)
            if whichperson[ind] == 'self':
                instext_self.setAutoDraw(True)
                title_emo.setAutoDraw(True)
            if whichperson[ind] == 'partner':
                instext_partner.setAutoDraw(True)
                title_emo_partner.setAutoDraw(True)
            hint.setAutoDraw(True)
            title.setAutoDraw(False)
            ratingScale.setAutoDraw(False)
            handle.setAutoDraw(False)
            label1.setAutoDraw(False)
            label2.setAutoDraw(False)
            #remind.setAutoDraw(False)
            mov.pause()
            mov.setAutoDraw(False)
            mov.status = PAUSED
            #inputtext = event.getKeys()
            #textbox.setText(inputtext)
            #event.waitKeys(keyList=['tab'])
    if event.getKeys(['tab']):
        movtime.addTime(-pausetime.getTime())
        mov.play()
        mov.setAutoDraw(True)
        textbox.setAutoDraw(False)
        instext_self.setAutoDraw(False)
        instext_partner.setAutoDraw(False)
        title_emo_partner.setAutoDraw(False)
        title_emo.setAutoDraw(False)
        hint.setAutoDraw(False)
        title.setAutoDraw(True)
        ratingScale.setAutoDraw(True)
        handle.setAutoDraw(True)
        label1.setAutoDraw(True)
        label2.setAutoDraw(True)
        #remind.setAutoDraw(True)
        textbox.text = ""

#########################################
#Alert participants that they are done with the task

win.flip()

ratingScale.setAutoDraw(False)
handle.setAutoDraw(False)
label1.setAutoDraw(False)
label2.setAutoDraw(False)
title.setAutoDraw(False)
mov.setAutoDraw(False)
#remind.setAutoDraw(False)

end_txt = "You are all done with this task! Please open the door to alert the experimenter and then remain seated until they arrive."
end=psychopy.visual.TextStim(win=win,alignText='center', anchorHoriz='center',text=end_txt,color=[1, 1, 1],height=30,pos=[0,0],wrapWidth=1000)

end.draw()
win.flip()
psychopy.event.waitKeys(keyList=['escape'])

#########################################
#SHUT DOWN
output_csv.close()
win.close()
core.quit()
