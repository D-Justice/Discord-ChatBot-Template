import requests
import json
from config import *
import websockets as ws
import asyncio
import sys
import random
import pickle
import re
from urllib.parse import quote
import base64
#jprint will print json data in the correct format to make it easy to read
def jprint(obj):

    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
#send_opResponse sends required op code when the web server asks for it
def send_opResponse():
    return json.dumps({
        "op": 2,
        "d": {
            "token": bot_token,
            "intents": 513,
            "properties": {
                "$os": "windows",
                "$browser": "my_library",
                "$device": "my_library"
            }
        }
    })
#base url is the main endpoint used for this bot to send messages
baseURL = f"https://discordapp.com/api/channels/{channel_id}/messages"
headers = {
    "Authorization": "Bot {}".format(bot_token),
    "Content-Type": "application/json",
}
#send(message) is used to send content
def send(message):
    r = requests.post(baseURL, headers = headers, data = json.dumps({"content":message}))
    return r.json()
#embed(content) is used to send embedded content
def embed(content):
    r = requests.post(baseURL, headers = headers, data = json.dumps(content))
    return r.json()
#The following functions are template abilities of the bot, feel free to change these at will
def send_tron_dump():
    global quote_url
    tronald_api = "https://matchilling-tronald-dump-v1.p.rapidapi.com/random/quote"
    tronald_headers = {
        'accept': 'application/hal+json',
        'x-rapidapi-key': trump_key,
        'x-rapidapi-host': "matchilling-tronald-dump-v1.p.rapidapi.com"
    }
    
    req = requests.get(tronald_api, headers=tronald_headers)
    quotee = req.json()['_embedded']['author'][0]['name']
    quote_url = req.json()['_embedded']['source'][0]['url']
    message = req.json()['value']
    format_message = (f'"{message}" - {quotee}')
    
    try:
        send(format_message)
    except Exception as i:
        print(i)
def trump_source():
    global quote_url
    print(quote_url)
    send(quote_url)
def advice():
    url = "https://api.adviceslip.com/advice"
    
    print('advice')
    r = requests.get(url)
    messo = r.json()['slip']['advice']
    send(messo)
def joke():
    jokes = ['Yo momma so dumb, she tried to surf the microwave','Teacher: How much is a gram?\nTyronne: Uhmm, depends on what you need',
    'Why are frogs always so happy? They eat what ever bugs them',
    'Some guy called me a tool. So I got hammered and nailed his girlfriend. Guess he was right.',
    'Yo mama is so ugly she made my happy meal cry',"I couldn't figure out why the baseball kept getting larger. Then it hit me.",
    "Yo mama so fat, she doesnt need internet, she's already worldwide.",
    "The energizer bunny was arrested on a charge of battery.",
    'I named my hard drive "dat ass," so once a month my computer asks if I want to "back dat ass up."']
    joke = "" 
    joke += random.choice(jokes)
    send(joke)
def create_channel():
    global channel_id
    value = False
    skip = False
    for users in channel_creators:
        print(users)
        if username == users['Username']:
            print(users['Username'])
            channel_name = users['Channel_Name']
            send(f"Please delete '{channel_name}' before creating another one")
            value = True
            pass
        else:
            continue
    if value == True:
        print('passing')
        pass
    else:
        channel_types = {
            'text': 0,
            'dm': 1,
            'voice': 2,
            'group': 3
        }
        if message_list[2] != 'text' and message_list[2] != 'voice':
            send('Please enter correct channel type(text OR voice')
            pass
        else:
            chan_type = channel_types.get(message_list[2])
            global chan_name
            chan_name = message_list[1]
            url = f'https://discordapp.com/api/guilds/{server_id}/channels'
            parameters = json.dumps({
                'name': chan_name,
                'type': chan_type 
            })
            r = requests.post(url, headers=headers, data=parameters)
            
            channel_id = r.json()['id']
            channel_creators.append({'Username': f"{username}","Channel_Name": f"{chan_name}","Channel_ID": f"{channel_id}"})
            file = open('record', 'wb')
            pickle.dump(channel_creators, file)
            file.close()

            
            #jprint(channel_creators)
            try:
                send(f"Created '{chan_name}' {message_list[2]} channel")
                
                pass
            except Exception as i:
                print(i)
def delete_channel():
    count = 0

    for obj in channel_creators:
        if username == obj['Username']:
            if message_list[1] == obj['Channel_Name']:
                channel_name = obj['Channel_Name']
                channel_id = obj['Channel_ID']
                print('object')
                print(obj)
                channel_creators.remove(channel_creators[count])
            else:
                continue
        else:
            count +=1
            continue
    if message_list[1] != channel_name:
        send(f'That is not your channel sorry. You can only delete {chan_name}')
        pass
    else:
        send(f"'{channel_name}' channel was deleted!")
        url = f'https://discordapp.com/api/channels/{channel_id}'
        delete = requests.delete(url, headers=headers)
        file = open('record', 'wb')
        pickle.dump(channel_creators, file)
        file.close()
        #print(delete.text)
def help_message():
    HELP = {
    "content": f"**UNRECOGNISED COMMAND**:\n\n",
    "embed": {
        # "title": f"{line['internalName']}",
        "description": "__**Commands:**__\n\n`!create [Channel name] [Channel type]`: Creates a channel\n\n`!delete [Channel name]`: Deletes your previously created channel\n\n`!advice`: Returns a random piece of advice\n\n`!deal [Top Price] [Return #] (opt)[nt - no thumbnail]`: Returns list of current video game deals\n\n`!sale [Game name] [Return #]`: Returns best prices for first game\n\n`!tronald`: Returns random Donald Trump quote\n\n`!source`: Will display the source of the quote\n\n`!schedule format`:  Will display required schedule submission format\n\n`!schedule show`: Will show your input schedule\n\n`!schedule delete`: Will delete your schedule so you can input another one\n\n`!schedule compare`: Will compare all available schedules and output times that everyone is free\n\n`!help`: Will bring up this message again",
        # "url": f'{link}',
        "color": 15158332,
        "image": {
        "url": f""
        }
    }
    }
    embed(HELP)
    #send("**UNRECOGNISED COMMAND**:\n\nCommands:\n\n`!create [Channel name] [Channel type]`: Creates a channel\n\n`!delete [Channel name]`: Deletes your previously created channel\n\n`!advice`: Returns a random piece of advice\n\n`!deal [Top Price] [How many] (opt)[nt - no thumbnail]`: Returns list of current video game deals\n\n`!sale [Game name] [How many]`: Returns best prices for first game\n\n`!tronald`: Returns random Donald Trump quote\n\n`!source`: Will display the source of the quote\n\n`!help`: Will bring up this message again")
def ask_help():
    HELP = {
    "content": f"**HELP MENU**:\n\n",
    "embed": {
        # "title": f"{line['internalName']}",
        "description": "__**Commands:**__\n\n`!create [Channel name] [Channel type]`: Creates a channel\n\n`!delete [Channel name]`: Deletes your previously created channel\n\n`!advice`: Returns a random piece of advice\n\n`!deal [Top Price] [Return #] (opt)[nt - no thumbnail]`: Returns list of current video game deals\n\n`!sale [Game name] [Return #]`: Returns best prices for first game\n\n`!tronald`: Returns random Donald Trump quote\n\n`!source`: Will display the source of the quote\n\n`!schedule format`:  Will display required schedule submission format\n\n`!schedule show`: Will show your input schedule\n\n`!schedule delete`: Will delete your schedule so you can input another one\n\n`!schedule compare`: Will compare all available schedules and output times that everyone is free\n\n`!help`: Will bring up this message again",
        # "url": f'{link}',
        "color": 15158332,
        "image": {
        "url": f""
        }
    }
    }
    embed(HELP)
    #send("**HELP MENU**:\n\nCommands:\n\n`!create [Channel name] [Channel type]`: Creates a channel\n\n`!delete [Channel name]`: Deletes your previously created channel\n\n`!advice`: Returns a random piece of advice\n\n`!deal [Top Price] [How many] (opt)[nt - no thumbnail]`: Returns list of current video game deals\n\n`!sale [Game name] [How many]`: Returns best prices for first game\n\n`!tronald`: Returns random Donald Trump quote\n\n`!source`: Will display the source of the quote\n\n`!help`: Will bring up this message again")
def sales():
    
    title = message_list[1]
    try:
        iterations = int(message_list[2])
    except:
        iterations = 5
    sales_list = requests.get(f"https://www.cheapshark.com/api/1.0/games?title={title}&limit=10&exact=0")
    deal_location = "https://www.cheapshark.com/api/1.0/games?id="
    steamStore = "https://store.steampowered.com/app/"
    deal_lookup = "https://www.cheapshark.com/api/1.0/deals?id="
    cheapest = "https://www.cheapshark.com/redirect?dealID="
    jprint(sales_list.json())
    count = 0
    for deals in sales_list.json():
        # date = deals['lastChange']
        jprint(deals)
        if count >= iterations:
            pass
        else:
            try:
                lookup = requests.get(deal_lookup + deals['cheapestDealID'])
                store = (lookup.json()['gameInfo']['storeID'])
                store = stores.get(store)
                AUD = round(float(deals['cheapest']) * 1.5, 2)
                enc_gametitle = quote(deals['external'], safe='')
                link = cheapest + deals['cheapestDealID'] 
                print('made')
                embedded = {
                        "content": f"{deals['external']} --Sales Price: ${AUD} \n{link + '>'}\nFound from: {store}",
                        "embed": {
                            # "title": f"{line['internalName']}",
                            # "description": f"AUD Price: ${sales_aud}\nUsual price: ${reg_aud}",
                            # "url": f'{link}',
                            # "color": 16777215,
                            "image": {
                            "url": f"{deals['thumb']}"
                            }
                        }
                        }
                embed(embedded)
                count += 1
                time.sleep(2)

            except:
                print('failed')
                
                continue
def deals():
    price = message_list[1]
    url = f"https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice={price}"
    payload = {
        'desc': 1,
    }
    files = {}
    headers = {}
    steamStore = "<https://store.steampowered.com/app/"
    deal_lookup = "https://www.cheapshark.com/api/1.0/deals?id="
    cheapest = "https://www.cheapshark.com/redirect?dealID="
    response = requests.get(url)
    count = 0
    try:
        nothumb = message_list[3]
    except:
        nothumb = ""
    try:
        iterations = int(message_list[2])
    except:
        iterations = 5
    try:
        if nothumb == "nt":
    
            short_list = ""
            
            for line in response.json():
                jprint(line)
                if count >= iterations:
                    pass
                else:
                    lookup = requests.get(deal_lookup + line['dealID'])
                    store = (lookup.json()['gameInfo']['storeID'])
                    store = stores.get(store)
                    enc_gametitle = quote(line['title'], safe='')
                    sales_aud = round(float(line['salePrice']) * 1.5, 2)
                    reg_aud = round(float(line['normalPrice']) * 1.5, 2)
                    link = '<' + cheapest + line['dealID'] + '>'
                    no_thumb = (f"{line['title']}: --Sale Price: ${sales_aud}, --Reg Price: ${reg_aud}\n{link}\nFound from: {store}")
                    short_list += no_thumb + "\n\n"
                    count += 1
           
            try:      
                send(short_list)
            except Exception as i:
                print(i)
    
        else:
            
            for line in response.json():
                try:
                    if count >= iterations:
                        print('passed')
                        pass
                    else:
                        lookup = requests.get(deal_lookup + line['dealID'])
                        store = (lookup.json()['gameInfo']['storeID'])
                        store = stores.get(store)
                        enc_gametitle = quote(line['title'], safe='')
                        #jprint(line)
                        sales_aud = round(float(line['salePrice']) * 1.5, 2)
                        reg_aud = round(float(line['normalPrice']) * 1.5, 2)
                        link = '<' + cheapest + line['dealID'] + '>'
                        
                        try:
                            embedded = {
                                    "content": f"{line['title']} --Reg Price: ${reg_aud}, --Sales Price: ${sales_aud} \n{link + '>'}\nFound from: {store}",
                                    "embed": {
                                        # "title": f"{line['internalName']}",
                                        # "description": f"AUD Price: ${sales_aud}\nUsual price: ${reg_aud}",
                                        # "url": f'{link}',
                                        # "color": 16777215,
                                        "image": {
                                        "url": f"{line['thumb']}"
                                        }
                                    }
                                    }
                            
                        except Exception as i:
                            print(i)
                        try:
                            
                            embed(embedded)
                            count += 1
                            time.sleep(2)
                        except Exception as i:
                            print(i)
                except Exception as i:
                    print(i)
    except Exception as i:
        print(i)
def scheduleTime():
    user,Sun,M,T,W,Thurs,F,S = [],[],[],[],[],[],[],[]
    user.append(username)
    currentScheds = []
    
    #if file exists, opens existing schedule inputs and saves them into currentScheds
    #otherwise it creates the new file later on
    try:
        file = open('schedules', 'rb')
        currentScheds = pickle.load(file)
        file.close()
        
        print('current user is:', username)
        
    except:
        print('no file found, creating...')
       
    if message_list[1] == 'deleteme':
        x = 0
        tempList = []
        try:
            
            for deleteUser in currentScheds:
                deleteUser = str(deleteUser[0])
                if message_list[2] == deleteUser:
                    del currentScheds[x]
                    deleteUser = deleteUser.replace("'","")
                    deleteUser = deleteUser.replace("[","")
                    deleteUser = deleteUser.replace("]","")
                    send(f"{deleteUser}'s schedule was deleted")
                else:

                    x += 1
        except:
            x = 0
            for users in currentScheds:
                if users[0] == user:
                    
                    del currentScheds[x]
                    send(f"{username}'s schedule was deleted")
                else:
                    x += 1
                    continue
        try:
            file = open('schedules', 'wb')
            pickle.dump(currentScheds, file)
            file.close()
        except:
            pass
    elif message_list[1] == 'deleteall':
        currentScheds.clear()
        file = open('schedules', 'wb')
        pickle.dump(currentScheds, file)
        file.close()
        send('All schedules deleted')
    elif message_list[1] == 'show':
        users = username
        try:
            if message_list[2]:
                users = message_list[2]
                users = users.replace("'","")
                users = users.replace("[","")
                users = users.replace("]","")
            
        except:pass
        send(f'Current Schedules for {users}:\n')
        try:
            
            for users in currentScheds:
                try:
                    try:
                        
                        if str(users[0]) == message_list[2]:
                            days = -1
                            for times in users:
                                try:
                                    days += 1
                                    print(times)
                                    timeConversion(times,days)
                                except Exception as i:
                                    if times == user:
                                        print(i)
                                        pass
                                    else:
                                        times = [ 0 , 0 ]
                                        timeConversion(times, days)
                        else:
                            continue
                    except:
                        pass
                        if users[0] == user:
                            days = -1
                            for times in users:
                                try:
                                    days += 1
                                    print(times)
                                    timeConversion(times,days)
                                except Exception as i:
                                    if times == user:
                                        print(i)
                                        pass
                                    else:
                                        times = [ 0 , 0 ]
                                        timeConversion(times, days)
                                        
                        else:
                            continue
                    
                except:
                    noSched = {
            "content": f"",
            "embed": {
                # "title": f"{line['internalName']}",
                "description": f"No schedule found...",
                # "url": f'{link}',
                "color": 15158332,
                "image": {
                "url": f""
                }
            }
            }
                    embed(noSched)
                    pass
        except:
            pass
    elif message_list[1] == 'format':
        schedsFormat = {
            "content": f"**Schedule Format**:\n\n",
            "embed": {
                # "title": f"{line['internalName']}",
                "description": f"!schedule\n\nSun:0000-0000\n\nM:0000-0000\n\nT:0000-0000\n\nW:0000-0000\n\nThurs:0000-0000\n\nF:0000-0000\n\nS:0000-0000",
                # "url": f'{link}',
                "color": 15158332,
                "image": {
                "url": f""
                }
            }
            }
        embed(schedsFormat)
    elif message_list[1] == 'compare':
        try:
            fCount = -1
            sCount = 0
            fS, fM, fT, fW, fThur, fF, fSat = [], [], [], [], [], [], []
            sS, sM, sT, sW, sThur, sF, sSat = [], [], [], [], [], [], []
            fDayLists = {0 : fS, 1 :fM, 2 : fT, 3 : fW, 4 : fThur, 5 : fF, 6 : fSat}
            sDayLists = {0 : sS, 1 :sM, 2 : sT, 3 : sW, 4 : sThur, 5 : sF, 6 : sSat}
            for users in currentScheds:
                fCount = -1
                sCount = 0
                for times in users:
                    try:
                        if fCount == -1:
                            fCount += 1
                            pass
                        else:
                            fDayList = fDayLists.get(fCount)
                            sDayList = sDayLists.get(sCount)
                            fDayList.append(times[0])
                            sDayList.append(times[1])
                            fCount += 1
                            sCount += 1 
                    except:
                        print('No number found, passing')
                        fDayList.append('N/A')
                        sDayList.append('N/A')
                        fCount += 1
                        sCount += 1 
                        pass
                
            timeConversion([max(fS),min(sS)], 1)
            timeConversion([max(fM),min(sM)], 2)
            timeConversion([max(fT),min(sT)], 3)
            timeConversion([max(fW),min(sW)], 4)
            timeConversion([max(fThur),min(sThur)], 5)
            timeConversion([max(fF),min(sF)], 6)
            timeConversion([max(fSat),min(sSat)], 7)
        except:
            send('No schedules found')
    else:
        skip = False
        try:
            for users in currentScheds:
                print('users are',users[0])
                if users[0] == user:
                    print('found')
                    send('Schedule already exists for user, please delete and re-submit')
                    skip = True
                else:
                    print('not found')
                    skip = False
        except:
            print('No previous schedules found')
        if skip:
            print('Passed')
            pass
            
        else:
            try:
                days = 0
                for message in message_list:
                    
                    #print(message)
                    if message[:3] == 'Sun':
                        time = message[4:13]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        Sun.append(t1)
                        Sun.append(t2)
                        #print(W)
                    elif message[0] == 'M':
                        time = message[2:11]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        M.append(t1)
                        M.append(t2)
                        #print(M)
                    elif message[:5] == 'Thurs':
                        time = message[6:15]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        Thurs.append(t1)
                        Thurs.append(t2)
                        #print(W)
                    elif message[0] == 'T':
                        time = message[2:11]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        T.append(t1)
                        T.append(t2)
                        #print(T)
                    elif message[0] == 'W':
                        time = message[2:11]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        W.append(t1)
                        W.append(t2)
                        #print(W)
                    
                    elif message[0] == 'F':
                        time = message[2:11]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        F.append(t1)
                        F.append(t2)
                        #print(W)
                    elif message[0] == 'S':
                        time = message[2:11]
                        t1 = time[0:4]
                        t2 = time[5:9]
                        S.append(t1)
                        S.append(t2)
                        #print(W)
                    else:
                        print('No time found')
                    
                schedule = [user,Sun,M,T,W,Thurs,F,S]
                try:
                    timeConversion(Sun, days)
                    timeConversion(M, days)
                    timeConversion(T, days)
                    timeConversion(W, days)
                    timeConversion(Thurs, days)
                    timeConversion(F, days)
                    timeConversion(S, days)
                except Exception as i:
                    print(i)
                print('schedule: ',schedule)
            except Exception as i:
                print(i)
                send('Wrong format')
                pass
                
            try:
                currentScheds.append(schedule)
                
                try:
                    file = open('schedules', 'wb')
                    pickle.dump(currentScheds, file)
                    file.close()
                    send('Schedule Recieved')
                except:
                    print('File already created')
            except:
                pass
    
    #print(schedule)
def timeConversion(time,days):
    
    firstTime = time[0]
    secondTime = time[1]
    print(firstTime, secondTime)
    convert(firstTime,secondTime,days)
def convert(first,second,days):
    #firstnumber
    if first == '0000':
        first = 1200
        first = str(first)
        first = first[:2] + ':' + first[2:] + 'AM'
        pass
    elif first == 0 or second == 0:
        first = 'N/A'
        second = 'N/A'
    
    if message_list[1] == 'compare':
        if first >= second:
            first = 'No times available'
            second = ''
    try:
        global time
        if int(first) >= 1200:
            PM = True
        else:
            PM = False
        if int(first) >= 1300:
            first = int(first) - 1200
        else:
            first = int(first)
        
        if first >= 1000:
            first = str(first)
            first = first[:2] + ':' + first[2:]
            
        else:
            first = str(first)
            first = first[:1] + ':' + first[1:]
        if PM:
            first += 'PM'
        else:
            first += 'AM'
    except:
        print('Failed AM')
        #second number
    try:
        if second == '0000' or second =='2400':
            second = 1200
            second = str(first)
            #second = first[:2] + ':' + first[2:] + 'AM'
            pass
        if int(second) >= 1200:
            PM = True
        else:
            PM = False
        if int(second) >= 1300:
            second = int(second) - 1200
        else:
            second = int(second)
        
        if second >= 1000:
            second = str(second)
            second = second[:2] + ':' + second[2:]
            
        else:
            second = str(second)
            second = second[:1] + ':' + second[1:]
        if PM:
            second += 'PM'
        else:
            second += 'AM'
    except Exception as i:
        print(i)
        pass
        
    
    day = {1: 'Sunday: ', 2 : 'Monday: ', 3 : 'Tuesday: ', 4 : 'Wednesday: ', 5 : 'Thursday: ', 6 : 'Friday: ', 7 : 'Saturday: '}
    try:
        today = day.get(days)
        time = today + first + '-' + second
    except:
        time = first + '-' + second
    try:
        if days == 1:
            global scheduleShow
            scheduleShow = []
            scheduleShow.append(time)
            
            print('scheduleshow: ', scheduleShow)
        else:
            scheduleShow.append(time)
            print('scheduleshow: ', scheduleShow)
    except:
        pass
    try:
        if days == 7:
            scheduleDisplay = '\n\n'.join(scheduleShow)
            print(scheduleDisplay)
            if message_list[1] == 'show':
                users = username
                try:
                    if message_list[2]:
                        users = message_list[2]
                        users = users.replace("'","")
                        users = users.replace("[","")
                        users = users.replace("]","")
                    else:pass
                except:pass

                scheduleDisplayEmbeded = {
        "content": f"**{users}'s FREE TIME**:\n\n",
        "embed": {
            # "title": f"{line['internalName']}",
            "description": f"{scheduleDisplay}",
            # "url": f'{link}',
            "color": 15158332,
            "image": {
            "url": f""
            }
        }
        }   
            elif message_list[1] == 'compare':
                scheduleDisplayEmbeded = {
        "content": f"**Available times this week**:\n\n",
        "embed": {
            # "title": f"{line['internalName']}",
            "description": f"{scheduleDisplay}",
            # "url": f'{link}',
            "color": 15158332,
            "image": {
            "url": f""
            }
        }
        } 
            embed(scheduleDisplayEmbeded)
        else:
            pass
    except Exception as i:
        print(i)
        
        send(time)
    # try:
    #     send(scheduleShow)
    #     #print('Made it')
    # except:
    #     send(time)

    

#heartbeart() sends required op code when the web server asks for it
def heartbeat():
    
    return json.dumps({
        "op": 1,
        "d": last_sequence 
     })
#the functions dictionary below is used to reference the previous functions from the discord channel
#the server will pull the first word after the '!' character and link it to its function through this dictionary.
#To use, just change or add a key & value to your 'key word' and 'function name' and it should just work.
functions = {'schedule': scheduleTime, 'deal': deals, 'sale': sales, 'delete': delete_channel, 'create': create_channel,'jokes': joke, 'tronald': send_tron_dump, 'advice': advice, 'source': trump_source, 'help': ask_help}
global stores
#The following stores dictionary is used in conjunction with with the deals() function to reference the store id 
#to the accompanied store.
stores = {'1':'Steam','2':'GamersGate','3':'GreenManGaming','4':'Amazon','5':'GameStop','6':'Direct2Drive','7':'GoG','8':'Origin','9':'Get Games','10':'Shiny Loot','11':'Humble Store','12':'Desura','13':'Uplay','14':'IndieGameStand','15':'Fanatical','16':'Gamesrocket','17':'Games Republic','18':'SilaGames','19':'Playfield','20':'ImperialGames','21':'WinGameStore','22':'FunStockDigital','23':'GameBillet','24':'Voidu'}

#channel_creators is used to store the list of creators who have created a channel to stop them from creating a second channel 
#before deleting the second one
channel_creators = []
        
#SEND_CONTENT() keeps a connection open to the discord server and listens for activity
async def SEND_CONTENT(uri):
    global username
    global last_sequence
    global message_list
    global channel_creators
    last_sequence = None
    async with ws.connect(uri) as websocket:
        
        await websocket.send(send_opResponse())
        timer = 40
        
        print('Starting server....')
        try:
            #The following will load the list of channel creators (if it exists)
            file = open('record', 'rb')
            channel_creators = pickle.load(file)
            file.close()
            print(channel_creators)
        except:
            print('No file found, passing')
        while True:  
            #This while True loop will effectively listen and deconstruct each message sent through 
            #the discord channel with the appropriate starting character. In this case, '!'
            try:
                greeting = await asyncio.wait_for(websocket.recv(), timeout=0.25)
                greeting = json.loads(greeting)
                
                try:
                    
                    message_content = greeting['d']['content']
                    op_response = greeting['op']
                    
                    username = greeting['d']['author']['username']
                    
                    last_sequence = greeting['s']
                    
                    if message_content[0] == '!':
                        
                        message_content = message_content.replace('!','')
                        message_list = message_content.split()
                        message_content = message_list[0]
                        print(message_list)
                        key_word = ""
                        key_word += message_content
                        function_pick = functions.get(key_word)
                        try:
                            
                            function_pick()
                        except Exception as i:
                            if message_list[0] == 'delete':
                                send(f'Delete function can only delete channels you have created')
                                pass
                            else:
                                help_message()
                                print("cannot process")
                    else:
                        print('Does not begin with "!"')
                    if op_response == 9:
                        print('Recieved op 9')
                    elif op_response == 9:
                        print('Recieved op 9')
                    elif op_response == 10:
                        heart_interval = greeting['d']['']
                    else:
                        print(f'Recieved unknown op code {op_reponse}')
                except:
                    continue
                print('timeout ')
            #TimeoutError will, when timer hits 0, send the heartbeat data to the discord server
            except asyncio.TimeoutError:
                timer -= 0.25
                
                if timer <= 0:
                    try:
                        await websocket.send(heartbeat())
                    except Exception as i:
                        print(i)
                    #print('Hearbeat sent')
                    timer = 40
                    continue
                continue         
gateway = requests.get('https://discord.com/api/v8/gateway/bot', headers=headers)  
    
asyncio.get_event_loop().run_until_complete(SEND_CONTENT(gateway.json()['url'] + "?v=8&encoding=json"))