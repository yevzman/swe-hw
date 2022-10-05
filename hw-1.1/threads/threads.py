import threading

THREAD_COUNT = 3


def print_values_n_times(cond: threading.Condition, n: int, thread_count):
    global currentThreadNum

    for i in range(n):
        with cond:
            cond.wait_for(lambda: threading.current_thread().name == str(currentThreadNum))

            print(currentThreadNum + 1, end='')

            # after cTN changes, notify all threads to check statement
            currentThreadNum = (currentThreadNum + 1) % THREAD_COUNT  
            cond.notify_all()


currentThreadNum = 0
n = int(input())

condition = threading.Condition(lock=threading.Lock())
threadPool = [threading.Thread(name=str(i), target=print_values_n_times, args=(condition, n, THREAD_COUNT))
              for i in range(THREAD_COUNT)]

for i in range(THREAD_COUNT):
    threadPool[i].start()

for i in range(THREAD_COUNT):
    threadPool[i].join()

print()
