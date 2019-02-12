import nexmo
from threading import Timer,Thread
import time
import key
from pprint import pprint

client = nexmo.Client(
    application_id=key.applicationId,
    private_key=key.privateKey,
)

isCalling = False
CALL_INTERVAL = 15
def delay():
    global isCalling
    isCalling = True
    time.sleep(CALL_INTERVAL)
    isCalling = False
def sendCall(phone,text):
    global isCalling
    isCalling = True
    print('call to {} with msg:{}'.format(phone,text))
    if isinstance(phone,str):
        phone = [phone]
    for p in phone:
        response = client.create_call({
        'to': [{'type': 'phone', 'number': p}],
        'from': {'type': 'phone', 'number': "12014739601"},
        'ncco': [
                    {
                    "action": "talk",
                    "text": text
                    }
                ]
        })
        pprint(response)
def call(phone, text):
    
    global isCalling
    if not isCalling:
        sendCall(phone,text)
        Thread(target=delay).start()
        
        
if __name__ == '__main__':
    while True:
        call(['66966494859'],'Help me')
    # Timer(5,call,('','')).start()