import os
import logging

from source import Source
from time import sleep
from cv2 import resize, medianBlur, imwrite
from threading import Thread

from queues import QUEUE_A
from queues import QUEUE_B


class Consumer(object):
    def __init__(self, max_frames: int) -> None:
        self.max_frames = max_frames
        self.frames_cnt = 0
        self.resize_ratio = 0.5
        self.median_kernel = 5

        self.dir = 'processed'
        self.file_format = 'png'

        self.is_running = True  # should be atomic
        self.thread = Thread(
            target=self.consume_thread,
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

    def consume_thread(self):
        while self.is_running:
            logging.info(f"Count: {self.frames_cnt}")
            image = QUEUE_A.get()
            try:
                image = resize(image, (0,0), fx=self.resize_ratio, fy=self.resize_ratio)
                image = medianBlur(image, self.median_kernel)
            except Exception as e:
                logging.error(str(e))

            QUEUE_B.put(image)
            self.frames_cnt += 1
            if self.frames_cnt >= self.max_frames:
                self.save_frames_and_exit()

    def save_frames_and_exit(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        while not QUEUE_B.empty():
            image = QUEUE_B.get()
            filename = f'{self.dir}/{QUEUE_B.qsize()}.png'
            logging.info(f"Saving {filename}")
            imwrite(filename, image)

        self.is_running = False
