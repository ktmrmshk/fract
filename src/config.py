import json

CONFIG=json.loads('''
{
    "db" : {
        "host": "rabbitmq",
        "port": 27017,
        "dbname": "fractdb",
        "coll_testgen": "testgen",
        "coll_run": "fret"
    },
    "mq" : {
        "host": "mongodb",
        "port": 5672,
        "queuename": "fractq"
    }
}
''')


