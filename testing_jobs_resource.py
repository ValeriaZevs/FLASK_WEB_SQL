from requests import get, post, delete

print(get('http://127.0.0.1:8080/api/v2/jobs').json()) #список работы

print(get('http://127.0.0.1:8080/api/v2/jobs/1').json()) #получить одну работу

print(get('http://127.0.0.1:8080/api/v2/jobs/666').json()) #такой работы нет

print(delete('http://127.0.0.1:8080/api/v2/jobs/2').json()) #удалить работу

print(delete('http://127.0.0.1:8080/api/v2/jobs/666').json()) #нет такой работы

print(post('http://127.0.0.1:8080/api/v2/jobs/7',
           json={'id': 7,
                 'job': 'Testing7',
                 'work_size': 1,
                 'collaborators': '7',
                 'content': 'testing posting7',
                 'is_finished': False,
                 'team_leader': 1}).json()) #добавить работу

print(post('http://127.0.0.1:8080/api/v2/jobs',
           json={'id': 30,
                 'team_leader': 1,
                 'job': 'Test api',
                 'work_size': 1,
                 'is_finished': True}).json()) #нет некоторых пунктов

print(get('http://127.0.0.1:8080/api/v2/jobs').json()) #список работ