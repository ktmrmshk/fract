import json

CONFIG=json.loads('''
{
    "db" : {
        "host": "rabbitmq",
        "port": 27017,
        "db_testgen": "testgen",
        "db_run": "fret"
    },
    "mq" : {
        "host": "mongodb",
        "port": 5672,
        "queuename": "fractq"
    }
}
''')


