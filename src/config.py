import json

CONFIG=json.loads('''
{
    "db" : {
        "host": "mongodb",
        "port": 27017,
        "db_testgen": "testgen",
        "db_run": "fret"
    },
    "mq" : {
        "host": "rabbitmq",
        "port": 5672,
        "queuename": "fractq"
    }
}
''')
