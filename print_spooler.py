import threading
from queue import Queue, PriorityQueue


class PrintSpooler:
    __instance = None
    __lock = threading.Lock()
    __print_queue = Queue()
    __priority_queue = PriorityQueue()

    def __new__(cls):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def add_to_queue(cls, message: str, priority: int = 0):
        with cls.__lock:
            if priority > 0:
                cls.__priority_queue.put((priority, message))
            elif priority < 0:
                raise ValueError("Priority must be greater than 0")
            else:
                cls.__print_queue.put(message)

    @classmethod
    def process_queue(cls):
        while not cls.__priority_queue.empty():
            _, item = cls.__priority_queue.get()
            print(item)
        while not cls.__print_queue.empty():
            item = cls.__print_queue.get()
            print(item)


# Example usage
if __name__ == "__main__":
    spooler = PrintSpooler()
    spooler.add_to_queue("Print job 1")  # Low priority
    spooler.add_to_queue("Print job 2", 1)       # High priority
    spooler.process_queue()
