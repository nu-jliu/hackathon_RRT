import threading

g_num = 0

# Creating a mutex is essentially a function via
LOCK = threading.Lock () 
def task1 ():
    # lock
    for i in range ( 1000000 ):
        LOCK.acquire() 
        global g_num
        g_num += 1
        print ( 'TASK1:' , g_num )
        # release lock
        LOCK.release()


def task2 ():
    for i in range ( 1000000 ):
        LOCK.acquire()
        global g_num
        g_num += 1
        print ( 'TASK2:' , g_num )
        LOCK.release()


if __name__ == "__main__" :
    first = threading.Thread ( target = task1 )
    second = threading.Thread ( target = task2 )
    first.start()
    second.start()