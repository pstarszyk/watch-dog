import os
from multiprocessing.managers import BaseManager
from multiprocessing import Queue


class BrokerManager(BaseManager):
    pass

BrokerManager.register('get_queue')


class Broker:
    """
    API for Broker implementation.
    """

    manager_cls = BrokerManager
    auth_key = os.environ.get('AUTH_KEY')
    broker_port = os.environ.get('BROKER_PORT')

    def __init__(self):
        self.manager_obj = None
        self.queue_proxy = None

    def expose(self):
        """
        Exposes queue object as AutoProxy on localhost. 
        """

        queue = Queue()
        self.manager_cls.register('get_queue', callable=lambda:queue)
        self._init_manager()
        self.manager_obj.get_server().serve_forever()
    
    def connect(self):
        """
        Connects to server and obtains proxy. 
        """

        self.manager_obj = None
        self.queue_proxy = None
        self._init_manager()
        self.manager_obj.connect()
        self.queue_proxy = self.manager_obj.get_queue()
    
    def put(self, msg):
        """
        Method that puts messages to shared queue. 
        """

        if self.queue_proxy is not None:
            self.queue_proxy.put(msg)

    def get(self):
        """
        Method that gets messages from shared queue. 
        """

        if self.queue_proxy is not None:
            return self.queue_proxy.get()
    
    def _init_manager(self):
        """
        Initiates a BaseManager object at the Broker object level.
        """

        self.manager_obj = self.manager_cls(
            address=('127.0.0.1', int(self.broker_port)), 
            authkey=bytes(self.auth_key, 'utf-8')
            )


if __name__ == "__main__":
    Broker().expose()