import json
import localstack_client.session as boto3
from pandas import DataFrame
from sqlalchemy import create_engine
import datetime as dt    

QUEUE_NAME = "login-queue"

postgres_user = 'postgres'
postgres_pswd = 'postgres'
postgres_db = 'postgres'
postgres_host = 'localhost'

postgres_table_name = 'user_logins'


def read_from_sqs():
    sqs = boto3.client("sqs")
    queue_url = sqs.create_queue(QueueName=QUEUE_NAME)["QueueUrl"]

    messages = []

    for _ in range(100):
        messages.append(json.loads(sqs.receive_message(QueueUrl=queue_url)['Messages'][0]['Body']))

    messages_df = DataFrame(messages)

    messages_df['masked_ip'] = messages_df['ip'].apply(hash)
    messages_df['masked_device_id'] = messages_df['device_id'].apply(hash)

    messages_df['create_date'] = dt.datetime.today().strftime("%m/%d/%Y")

    return  messages_df.drop(['ip', 'device_id'], axis = 1)


def write_to_postgres(messages_df):
    engine = create_engine('postgresql+psycopg2://' + postgres_user + ':' + postgres_pswd + '@' + postgres_host + ':5432/' + postgres_db)
    messages_df.to_sql(name = postgres_table_name, con = engine, if_exists = 'append', index = False)


def main():
    messages_df = read_from_sqs()
    write_to_postgres(messages_df)


if __name__ == "__main__":
    main()
