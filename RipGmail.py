'''

don't touch the code, unless yk what you are doing (or you're daniu)

!!Everything you need to modify is in the data.yaml that came with this script!!

'''

import yagmail
import yaml
import time
import requests
import datetime

RandomizeSubject = False
Counter = 0
#get data from yaml

try:
    with open("customize.yaml", 'r') as f:
        YamlInfo = yaml.safe_load(f)

        #setup info

        Subject = YamlInfo['subject']
        SendLimit = YamlInfo['SendTimes']
        
        HowManyWords = YamlInfo['WordCount']
        BBC = YamlInfo['AutoBCC']

        #credencials
        Mail = YamlInfo['LoginInfo'][0]
        MailPWD = YamlInfo['LoginInfo'][1]

        PPLToSpam = YamlInfo['PPLToSpam']
except:
    raise SystemExit("Could not load all info, Or file nonexistant. \nIf file corrupted, reinstall the applicatoin and reenter info. \nIf the file doesn't exist, make sure you are in the root directory of the python script.")


#test internet connection
try:
    requests.get("https://google.com")
except:
    raise SystemExit("Bruh turn on your wifi...")

#try to login
try:
    MailClient = yagmail.SMTP(Mail, MailPWD) 
except:
    raise SystemExit("Email failed to authenticate... Make sure the .yaml file has the correct credencials")

#confirm subject field, else send random word as subject
if Subject == "":
    RandomizeSubject = True

while (Counter < SendLimit or SendLimit == 0): #if you can still send

    if RandomizeSubject: #refresh subject EVERY TIME (im sorry im so mean)
        try:
            Subject = list(requests.get("https://random-word-api.herokuapp.com/word?number=1").json())[0]
        except:
            Subject = "daniu goes moo"

    try:
        Content = " ".join(list(requests.get(f"https://random-word-api.herokuapp.com/word?number={HowManyWords}").json())) #get counter words lol
    except:
        Content = "daniu goes moo" #just in case

    try:
        if BBC: #if you wanna spam yourself privately too
            MailClient.send(to=PPLToSpam, subject=Subject, contents=Content, bcc=Mail)
        else:
            MailClient.send(to=PPLToSpam, subject=Subject, contents=Content)
        
        print(f"Sent successfully at {str(datetime.datetime.now())}")

    except Exception as e:
        raise SystemExit("Mail not sent successfully, check internet connection... Or daily spam limit reached")

    Counter += 1 #update count

print(f"--Sent {Counter} messages!--")