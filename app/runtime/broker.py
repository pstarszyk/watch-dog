import os
from multiprocessing.managers import BaseManager
from multiprocessing import Queue


class BrokerManager(BaseManager):
    pass

BrokerManager.register('get_queue')


if __name__ == "__main__":
    queue = Queue()
    BrokerManager.register('get_queue', callable=lambda:queue)
    manager = BrokerManager(
        address=('127.0.0.1', int(os.environ.get('BROKER_PORT'))), 
        authkey=bytes(os.environ.get('AUTH_KEY'), 'utf-8')
        )
    server = manager.get_server()
    server.serve_forever()