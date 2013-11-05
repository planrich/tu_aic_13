
import requests
import settings
import json

def post(url, task, keyword):
    count = 0
    data = {'id': None,
            'task_description': 'Is ' + keyword + \
                    ' mentioned in this text positive, neutral or negative?',
            'task_text': task.paragraph,
            'answer_possibilities': ['Positive','Neutral','Negative'],
            'callback_link': settings.CALLBACK_LINK,
            'price': 11
           }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for i in range(1,4):
        data['id'] = str(task.id) + "_" + str(i)
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == requests.codes.ok:
            count += 1
    return count

