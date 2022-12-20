#!/usr/bin/env python
"""
@author: Grzegorz Wozniak
@date: 20.12.2022
"""

from time import sleep

from producer import Producer
from consumer import Consumer


def main():
    producer = Producer(width=1024, height=768, channels=3, interval_ms=50)
    consumer = Consumer(max_frames=100)

    while producer.is_running_thread() == True and consumer.is_running_thread() == True:
        sleep(1) # could wait on conditional variable

    producer.stop()
    consumer.stop()

if __name__=='__main__':
    main()