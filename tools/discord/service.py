from discord import MessageReference #pip install discord.py
import websocket #pip install websocket-client
import json
import threading
import time
import sys
import requests

running = False

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)
    
def heartbeat(interval, ws):
    print('Auto Chat begin')
    global running
    while running:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print('heartbeat sent')

def send_message(token, channel_id, message):
    try:

        url = f'https://discord.com/api/v9/channels/{channel_id}/messages' #input channel exp: .../1190017920013713531/...
        payload = { 
            "content" : {message} #input content message @username before the content message
        }

        headers = {
            "Authorization" : token
        }

        res = requests.post(url, payload, headers=headers)
    
    except Exception as e:
        print('Send Message', e)
    
def tooggle_running():
    global running
    running = not running
    print('running:', running)
    return running

def run(token, channel_id, history):
    global running

    if (running is False):
        return history

    send_message(token, channel_id=channel_id, message='Start Auto Chat')
    ws = websocket.WebSocket()

    ws.connect("wss://gateway.discord.gg")

    event = recieve_json_response(ws)

    heartbeat_interval = event['d']['heartbeat_interval'] / 1000
    threading._start_new_thread(heartbeat, (heartbeat_interval,ws))

    payload ={
        'op': 2,
        'd':{
            "token": token,
            "properties": {
                "$os":"windows",
                "$properties":"chrome",
                "$device":'chrome'
            }
        }
    }
    send_json_request(ws, payload)

    timer = 0

    

    while running:
        
        event = recieve_json_response(ws)

        # print('Waiting for message', event)
        try:
            content = event['d']['content']
            author = event['d']['author']['username']
            id = event ['d']['id']
            MessageReference = event ['d']['channel_id']
            MessageReference_1 = event['d']['guild_id']
            tinnhan=(f'guild_id:{MessageReference_1}|channel_id:{MessageReference}|userID:{id}|username: {author}|{content}')
            
            if channel_id in tinnhan:
                
                history += [[None, tinnhan]]
                yield history

            op_code = event('op')
            if op_code == 11:
                print('heartbeat recieved')
                
        except Exception as e:
            print(e)
            pass
    
    return history