from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Alex',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


def get_data():
    import requests
    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]
    return res


def format_data(res):
    data = {}
    location = res['location']
    data['id'] = uuid.uuid4()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data
    
def stream_data():
    import json
    res = get_data()
    res = format_data(res)
    print(json.dumps(res, indent=3))
    


with DAG('user_automation', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    streaming_task = PythonOperator(
        task_id='streaming_task',
        python_callable=stream_data,
        dag=dag
    )

get_data()