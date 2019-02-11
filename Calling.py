import nexmo
import key
from pprint import pprint

client = nexmo.Client(
    application_id=key.applicationId,
    private_key=key.privateKey,
)

def call(phone,text):
    if isinstance(phone,str) :
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
if __name__ == '__main__':
    call('66966494859','Help me')