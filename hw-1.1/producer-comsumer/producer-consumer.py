import threading

buffer = ''


def consumer(cond: threading.Condition, mutex: threading.Lock):
    global buffer
    while True:
        with cond:
            cond.wait_for(lambda: buffer != '')
            mutex.acquire()
            print('consumer got message:', buffer)
            print('===============================================')
            buffer = ''
            mutex.release()
            cond.notify_all()


def producer(cond: threading.Condition, mutex: threading.Lock):
    global buffer
    while True:
        with cond:
            mutex.acquire()
            buffer = input('Input message for producer sending: ')
            print('Producer get message:', buffer)
            print('storing....')
            mutex.release()
            cond.notify_all()
            cond.wait()


mutex = threading.Lock()
cond = threading.Condition()

cons = threading.Thread(target=consumer, args=(cond, mutex,))
prod = threading.Thread(target=producer, args=(cond, mutex,))

cons.start()
prod.start()
