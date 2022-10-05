import threading

buffer = ''


def consumer(cond: threading.Condition):
    global buffer
    while True:
        with cond:
            cond.wait_for(lambda: buffer != '')
            print('consumer got message:', buffer)
            print('===============================================')
            buffer = ''
            cond.notify_all()


def producer(cond: threading.Condition):
    global buffer
    while True:
        with cond:
            while not buffer:
                buffer = input('Input message for producer sending: ')

            print('Producer get message:', buffer)
            print('storing....')
            cond.notify_all()
            cond.wait()


cond = threading.Condition()

cons = threading.Thread(target=consumer, args=(cond,))
prod = threading.Thread(target=producer, args=(cond,))

cons.start()
prod.start()
