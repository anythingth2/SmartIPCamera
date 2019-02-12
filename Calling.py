import nexmo
from threading import Timer
import key
from pprint import pprint

client = nexmo.Client(
    application_id=key.applicationId,
    private_key=key.privateKey,
)

isCalling = False
CALL_INTERVAL = 10
def sendCall(phone,text):
    global isCalling
    
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
    isCalling = False
def call(phone, text):
    
    global isCalling
    if not isCalling:
        isCalling = True
        Timer(CALL_INTERVAL,sendCall,(phone,text)).start()
if __name__ == '__main__':
    while True:
        call(['66966494859'],'Help me')
    # Timer(5,call,('','')).start()