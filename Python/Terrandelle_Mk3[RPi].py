'''
Terandelle Mk3 [RPi]
'''
#
#
#
#
#
#
#
#importing libraries
print('importing libraries') 
#
import speech_recognition as sr
from gtts import gTTS
import os
import wikipedia
import re
from pyowm import OWM
import smtplib
import RPi.GPIO as GPIO
import threading
import sys
import vlc
import pafy
import random
import subprocess
import pygame
import time
#
#
#
'''
play audio from text input
'''
#function to play audio with text input
def terandelleResponse(audio):
    "speaks audio passed as argument"
    print("audio to speak: "+str(audio))
    textToSpeak = ""
    #save tts string to file "tts.mp3" and then play it
    for line in audio.splitlines():
        tts = gTTS(text=str(audio), lang='en', slow=False)
        tts.save('tts.mp3')
        #commands().speak()
        os.system('mpg123 tts.mp3')
#
#
#
#
#
'''
a type of simple printing function for displaying text through pygame... eventually
'''
def post(text):
	print(str(text))
#
#
#
#
#
#
#
'''
variable definitions
'''
post('Definiting initial variables')
loop = True
GPIO.setmode(GPIO.BOARD)
post('Setting up GPIO')
adminMode = False
initialNetData = False
initialLocData = False
user = 'guest'
TerrendelleLevel = "Terandelle Mk 3 [RPi]"
'''
end variable definitions
'''
#
#
#
#
#
#
#speech recognition system returns the text
def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        errors = ['...','I didn\'t quite get that','what?','could you say that again?','Chto?']
        errorValue = random.randint(0,len(errors)-1)
        terandelleResponse(errors[errorValue])
        command = myCommand();

    return command
#
#
#
#
#
#
#
#
#
#
#
#
#

'''
    take the speech recognition information and if a specific phrase is found in the command, perform a designated function 
'''
def assistant(command):
    securityLevel = 'black'
    global user
    global adminMode
    
    print(command)
    if "time" in command:
            timeText=('the current time is %d:%d' %(int(commands().time().hour),int(commands().time().minute)))
            print(timeText)
            terandelleResponse(timeText)
    
    elif 'define' in command:
        commands().define(command)

    elif 'what is the weather in' in command:
        commands().weather(command)

    elif 'google' in command:
        commands().googlele(command)
    
    elif 'shut down' in command or 'shutdown' in command or 'shuts down' in command:
        commands().shutdown()
        
    elif 'news' in command:
        commands().news()
        
    elif 'internet' in command:
        commands().internetStateResponse()
    
    elif 'search email for' in command:
            commands().emailCheck(command)
            
    elif 'activate sentry level green' in command:
        securityLevel = green
    
    elif 'activate sentry level amber' in command:
        securityLevel = amber
        
    elif 'wrath' in command or 'fury' in command:
        commands().wrathProtocal()
        
    elif 'music' in command:
        musicOrderArray = command.split(' ')
        musicOrder = musicOrderArray[0]
        commands().music(musicOrder)
        
    elif 'close program' in command or 'end program' in command:
        terandelleResponse('Ending program, have a nice day.')
        sys.exit()
        
    elif 'send email to' in command:
        terandelleResponse('who is this email for')
        Recipient = myCommand()
        recipient = Recipient
        if 'me' in recipient or 'myself' in recipient:
                recipient = 'codemaxx1@gmail.com'
                loop = True
        while loop:
            terandelleResponse('what do you want to say?')
            Message = myCommand()
            message = Message
            terandelleResponse('you said '+message+'is that correct?')
            YorN = myCommand()
            if 'yes' in YorN:
                loop = False
            elif 'no' in YorN:
                loop = True
                
        commands().email(message,recipient)
        
    elif 'change volume' in command or "set volume to" in command or 'change volume to' in command or 'set volume' in command:
        volumeCommand = command.split(' ')
        volume = volumeCommand[-1]
        commands().volume(volume)
        
    elif 'help' in command:
        commands().help()
       
    elif 'login' in command or 'user login' in command or 'logan' in command:
        user = commands().login(command)
        
    elif 'system call' in command:
        if(adminMode):
            commands().admin(command)
            
        else:
            terandelleResponse('Permission Denied.  User Login ' +user+' not recognized')
            
        
    greetings = ['hello','hi','good morning','good afternoon','good evening','priviet']
    for greetingi in greetings:
        if greetingi in command:
            commands().greeting()
            
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
class commands:

        def intro(self):
            terandelleResponse(
                "Hello, my name is Terrandelle.  I am a digital assistant capable of performing basic functions.  While I may not have a massive library of knowlege, you can ask me just about any question.  Using my SST, or speech to text recognition system, I will try my best to answer your question.")

        # return the current time
        def time(self):
            import datetime
            now = datetime.datetime.now()
            # print("current time is %d hours %d minutes" %(now.hour,now.minute))
            return now

        # takes a specific command phrase and searches wikipedia for it
        # then it sends that information to the tts function
        def define(self, command):
            print('wikipedia search starting')
            reg_ex = re.search('define (.*)', command)
            try:
                if reg_ex:
                    print('step2')
                    topic = reg_ex.group(1)
                    print('step2.1')
                    ny = wikipedia.page(topic)
                    print('step2.2')
                    defineText = (ny.content[:500].encode('utf-8'))
                    print('step2.3')
                    try:
                        defineTextList = defineText.split('.')
                        print('step3a')
                        for i in range(3):
                            terandelleResponse(defineTextList[i])
                    except:
                        defineTextList = defineText
                        print('step3b')
                        terandelleResponse(defineTextList)
                    print('step4')
            except Exception as e:
                print(e)

        # Take a specific location defined by a vocal command
        # and then find the weather data for that city
        #
        def weather(self, command):
            reg_ex = re.search('what is the weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
                obs = owm.weather_at_place(city)
                w = obs.get_weather()
                k = w.get_status()
                x = w.get_temperature(unit='fahrenheit')
                terandelleResponse(
                    'The current weather in %s is %s.  The temperature High and Low are %0.2f and %0.2f respectively.' % (
                    city, k, x['temp_max'], x['temp_min']))

        # opens the default web browser and searches a specific phrase
        #
        def google(self, command):
            import webbrowser
            search = command.strip('google')
            URLtext = ('https://www.google.com/search?q=%s' % search)
            webbrowser.open(URLtext)

        # causes the pi to shut down
        # also resets the GPIO pins
        def shutdown(self):
            #

            terandelleResponse('Goodby sir, have a nice day.')
            GPIO.cleanup()
            commands().log('Shutdown command\n\n\n')
            # sys.exit()
            os.system('shutdown now')

        # parses the first 10 headlines from Yahoo news
        #
        def news(self):
            import feedparser
            d = feedparser.parse('https://www.yahoo.com/news/rss')
            newsFeedList = []
            newsFeedDict = {}
            for post in d.entries:
                newsFeedList.append(post.title)
                # newsFeedDict[post.title]=post.
            for i in range(len(newsFeedList)):
                try:
                    terandelleResponse(str(newsFeedList[i]))
                except:
                    terandelleResponse('there was an error with converting the RSS feed title into a readable string')
                if i > 10:
                    break

        # pings the google server and returns 1 if it is able to ping
        # and returns a 0 if it cannot ping the google server
        def internetState(self):
            ping = os.system('ping -c 1 google.com')
            state = 0
            if ping == 0:
                state = 1
            elif ping == 1:
                state = 0

            return state

        def internetStateResponse(self):
            state = commands().internetState()
            if state == 1:
                print('internet active')
                terandelleResponse('internet active')
            elif state == 0:
                print('no internet')

                os.system('mpg321 noInternet.mp3')

        def lights(self, setting):
            #
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(37, GPIO.OUT)
            if setting == 1:
                GPIO.output(37, GPIO.HIGH)
                # lightState = 1
            elif setting == 0:
                GPIO.output(37, GPIO.LOW)
                # lightState = 0

        def emailCheck(self, command):
            from GmailWrapper import GmailWrapper
            title = command.replace('search email for ', '')
            try:
                gmailWrapper = GmailWrapper('imap.gmail.com', 'codemaxx1', 'boyscouts')
                ids = gmailWrapper.getIdsBySubject(str(title[:]))
            except:
                ids = 123456
            print('what you said to search for:' + str(title))
            print('search parameter:' + str(title[:]))
            number = 'no'
            try:
                if len(ids) > 0:
                    # gmailWrapper.markAsRead(ids)
                    number = 'indeed'
                    print('email return number', str(number))
            except:
                number = 'error searching'
            terandelleResponse('there are ' + str(number) + ' emails that match that title')

        def music(self, order):
            if order == "play":
                songURL = 'https://www.youtube.com/watch?v=hr23P9_DPwg'
                video = pafy.new(songURL)
                best = video.getbest()
                playurl = best.url

                Instance = vlc.Instance()
                player = Instance.media_player_new()
                Media = Instance.media_new(playurl)
                Media.get_mrl()
                player.set_media(Media)
                player.play()

        def email(self, message, recipient):
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('codemaxx1@gmail.com', 'boyscouts')
            mail.sendmail('codemaxx1@gmail.com', recipient, message)
            mail.close()

        def greeting(self):
            now = datetime.datetime.now()
            morningGreeting = ['Good Morning', 'Top of the morning to you', 'hello', 'morning', 'have a nice day']
            afternoonGreeting = ['afternoon', 'good afternoon', 'hello', 'hi']
            eveningGreeting = ['evening', 'good evening', 'hello', 'hi']
            # print("current time is %d hours %d minutes" %(now.hour,now.minute))
            time = now.hour
            if (time < 12):
                value = random.randint(0, len(morningGreeting) - 1)
                terandelleResponse(morningGreeting[value])

            if (time >= 12 and time <= 18):
                value = random.randint(0, len(afternoonGreeting) - 1)
                terandelleResponse(afternoonGreeting[value])

            if (time > 18):
                value = random.randint(0, len(eveningGreeting) - 1)
                terandelleResponse(eveningGreeting[value])

        def blackout(self):
            # wipe the operating system and all data on the device (have a backup system so that everythong doesn't get lost
            print('erasing data')

        # generates a log of the commands, tts, and stt information
        # generates both a log of all time, and of the prior session (wipes at the beginning of the session)
        fileStart = open('log_Unsaved.txt', 'w+')
        fileStart.close()
        file = open('log.txt', 'a')
        file.write(5 * '\n')
        file.close()

        def log(self, text):
            import datetime
            now = datetime.datetime.now()
            try:
                file = open('log.txt', 'a')
                file.write(str(text) + 5 * ' ' + str(now) + '\n')
                file.close()
            except:
                print("error: the log.txt file does not exit")

            try:
                file = open('log_Unsaved.txt', 'a')
                file.write(str(text) + 5 * ' ' + str(now) + '\n')
                file.close()
            except:
                print("error: the 'log_Unsaved.txt' file does not exit")

        # take a file named calendarSchedule.txt and check the current time / date to find if there is currently something scheduled
        # at this time.
        # and if there is indeed an event at this time, send it to tts to be spoken
        def calendar(self):
            import datetime
            now = commands().time()
            now = str(now.hour) + ':' + str(now.minute)
            file = open('calendarSchedule.txt', 'r')
            fileList = file.readlines()
            #
            print(now)
            for i in range(len(fileList)):
                # terandelleResponse(str(fileList[i]))
                # print(fileList[i])

                if now in fileList[i]:
                    print('Calender time and minute parameters met')
                    print(fileList[i])
                    terandelleResponse(str(fileList[i]))
            file.close()

        def wrathProtocal(self):
            terandelleResponse("Wrath and fury protocal activated")

        def volume(self, volume):
            global user
            global adminMode

            if int(volume.strip('%')) < 10 and adminMode == False:
                terandelleResponse('Permission Denied.  User Login ' + user + ' not recognized')
            else:
                volumeSet = ('sudo amixer cset numid=1 ' + str(volume))
                os.system(volumeSet)

        def help(self):
            commandList = ['Time:     Prints and uses TTS to tell you the current time (Hours:Minutes)',
                           'Define:     What you say after "define" is going to be searched through wikipedia and then both printed and TTS\'d to you',
                           'What is the Weather in:     Prints and uses TTS to tell you the weather and Hi/Low Temp.  The user must define which city immidiately after sayiung "What is the weather in"',
                           'Google:     Opens a Window of your default']
            for i in range(len(commandList)):
                print(commandList[i])
                terandelleResponse(commandList[i])

        def login(self, command):
            global user
            global adminMode
            userName = command.split(' ')
            # find user from file directory (d7-12)
            os.chdir('/home/pi/D-7-12')
            files = os.listdir()
            print(files)
            # 'login' in command or 'user login' in command or 'logan'
            if userName[0] == 'login' or userName[0] == 'logan':
                first = userName[1]
                last = userName[2]
            if userName[1] == 'login' or userName[1] == 'logan' or userName[1] == 'user':
                first = userName[2]
                last = userName[3]

            for person in files:
                if first in person and last in person:
                    # 'login' in command or 'user login' in command or 'logan'
                    terandelleResponse('welcome ' + str(first + " " + last))
                    user = first + ' ' + last
                    if (first == 'baker' or first == 'john') and (last == 'baker' or last == 'john'):
                        adminMode = True
                        user = 'John Baker'
            os.chdir('/home/pi')
            return user

        def admin(self, command):
            # d-7-12
            global user
            global adminMode
            terandelleResponse('Admin mode active')
            commandOrder = command.split(' ')

        def mood(self, color):
            green = 15
            blue = 11
            red = 13
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(green, GPIO.OUT)
            GPIO.setup(red, GPIO.OUT)
            GPIO.setup(blue, GPIO.OUT)
            if color == 'red':
                GPIO.output(red, GPIO.HIGH)
                GPIO.output(blue, GPIO.LOW)
                GPIO.output(green, GPIO.LOW)
                # lightState = 1
            elif color == 'green':
                GPIO.output(green, GPIO.HIGH)
                GPIO.output(red, GPIO.LOW)
                GPIO.output(blue, GPIO.LOW)

            elif color == 'blue':
                GPIO.output(blue, GPIO.HIGH)
                GPIO.output(red, GPIO.LOW)
                GPIO.output(green, GPIO.LOW)

            elif color == 'all':
                GPIO.output(blue, GPIO.HIGH)
                GPIO.output(red, GPIO.HIGH)
                GPIO.output(green, GPIO.HIGH)

            elif color == 'none':
                GPIO.output(blue, GPIO.LOW)
                GPIO.output(red, GPIO.LOW)
                GPIO.output(green, GPIO.LOW)
                # lightState = 0

        def speakFlash(self, length):
            import time
            startTime = float(time.time())
            deltaTime = float(time.time() - startTime)
            while deltaTime <= length:
                deltaTime = float(time.time() - startTime)
                commands().mood('green')
                time.sleep(0.1)
                commands().mood('none')
                time.sleep(0.1)

        def speak(self):
            duration = str(subprocess.check_output('ffprobe -show_entries format=duration -i tts.mp3', shell=True))
            durationList = duration.split('\\n')
            # durationList = durationList.split('')
            for i in range(len(durationList)):
                if 'duration' in str(durationList[i]):
                    length = float(durationList[i].strip('duration='))
                    print(' \n\n result:' + str(durationList[i]))
                    print(length)
                    break
            speakThread = threading.Thread(target=commands().speakFlash, args=(length,), daemon=True)
            speakThread.start()


# end of commands class
#
#
#
#
#
#
#
#
#
#
#
#
#
#
'''
initiate pygame
'''
post('pygame initializing')
pygame.init()
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
width = display_width
height = display_height
size = width,height
gameDisplay = pygame.display.set_mode(size)
#gameDisplay = pygame.display.set_mode(size,pygame.FULLSCREEN)
pygame.display.set_caption(TerrendelleLevel)
black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
'''
begin graphical bootup gui
'''
terandelleResponse("Configuring bootup data")
for j in range(1,int(display_width/5)):
    gameDisplay.fill((0,0,128))

    '''get network data'''
    if j > int(display_width / 10) and initialNetData == False:
        initialNetData = True
        terandelleResponse("getting network data")

    '''end getting network data'''

    '''get location data through IP'''
    if j > int(display_width / 16) and initialLocData == False:
        initialLocData = True
        terandelleResponse("getting location data")
        
    '''end getting location data through IP'''

    #                                                 x                       y   width  height
    pygame.draw.rect(gameDisplay,(77,106,255)  , (display_width/2 - int(j*5) ,0 ,j ,display_height) )
    pygame.display.flip()
    #pygame.display.update()
    clock.tick(60)
'''
end graphical GUI bootup
'''

#








#get location data
#get map of location
#
#
#
#
#

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(1)

x =  (display_width * 0.45)
y = (display_height * 0.8)
'''
end pygame initialization 
'''
#
#
#
#
#
'''
time initialization
'''
print('generating initial timestamp')
import datetime
now = datetime.datetime.now()
#print("current time is %d hours %d minutes" %(now.hour,now.minute))
time = now.minute
print('initial timestamp generated')
terandelleResponse('Ready to go.  Welcome user.')
'''
End time initialization
'''
#
#
#
#
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
    assistant(myCommand())
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
    gameDisplay.fill(black)

pygame.quit()
quit()
