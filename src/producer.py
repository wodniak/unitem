from source import Source
from time import sleep
from threading import Thread
import logging

from queues import QUEUE_A

class Producer(object):
    def __init__(self, width: int, height: int, channels: int, interval_ms: int) -> None :
        self.width = width
        self.heigh = height
        self.channels = channels
        self.interval_s = interval_ms / 1000

        self.source = Source((width, height, channels))

        self.is_running = True
        self.thread = Thread(
            target=self.produce_thread,
            daemon=False,
        )
        self.thread.start()

    def __del__(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

    def is_running_thread(self):
        return self.is_running

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

    def produce_thread(self):
        while self.is_running:
            image = self.source.get_data()
            QUEUE_A.put(image)
            # print(f"Produce {QUEUE_A.qsize()}")
            sleep(self.interval_s)
