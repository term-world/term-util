import threading

from time import sleep
from rich.spinner import Spinner
from rich.live import Live

class SpinThread(threading.Thread):

    def __init__(self):
        super().__init__(target=self.__spin)
        self.__stopevent = threading.Event()

    def stop(self):
        self.__stopevent.set()

    def __spin(self):
        with Live(
            Spinner('dots3', text = "Waiting for response...", style = "green")
        ) as live:
            while not self.__stopevent.isSet():
                sleep(0.1)
        print("🤖 cliv3: I found an answer! Check it out below.", end = "\n\n")

