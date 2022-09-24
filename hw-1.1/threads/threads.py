import threading


def print_values_n_times(n: int, cond: threading.Condition):
    global currentThreadNum

    for i in range(n):
        with cond:
            cond.wait_for(lambda: threading.current_thread().name == str(currentThreadNum))
            print(currentThreadNum + 1, end='')
            currentThreadNum = (currentThreadNum + 1) % 3  # after cTN changes, notify all threads to check statement
            cond.notify_all()


currentThreadNum = 0
n = int(input())

condition = threading.Condition(lock=threading.Lock())
threadPool = [threading.Thread(name=str(i), target=print_values_n_times, args=(n, condition, ))
              for i in range(3)]

for i in range(3):
    threadPool[i].start()

for i in range(3):
    threadPool[i].join()

print()
