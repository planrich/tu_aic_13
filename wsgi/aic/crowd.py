
import requests
import settings
import json

def post_task(task, keyword):
    url = settings.CROWD_DOMAIN + '/tasks'
    answers_requested = 0
    data = {'id': None,
            'task_description': 'Is ' + keyword.keyword + \
                    ' mentioned in this text positive, neutral or negative?',
            'task_text': task.paragraph,
            'answer_possibilities': ['Positive','Neutral','Negative'],
            'callback_link': settings.DOMAIN + '/api/tasks/' + str(task.id) + '/answers',
            'price': task.price
           }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for i in range(1,4):
        data['id'] = str(task.id) + "_" + str(i)
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == requests.codes.ok:
            answers_requested  += 1
    return answers_requested

def set_bonus(task):
    url = settings.CROWD_DOMAIN + '/set_bonus'
    data = {'id': None,
            'price_bonus': task.price_bonus
           }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for i in range(1,task.answers_requested+1):
        data['id'] =  str(task.id) + "_" + str(i)
        response = requests.post(url, data=json.dumps(data), headers=headers)
    return 0

