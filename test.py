from threading import Thread
import time
def f(n):
    time.sleep(1)
    print(n)



p1=Thread(target=f,args=(1,))
p1.start()
p2=Thread(target=f,args=(2,))
p2.start()