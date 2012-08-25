import time

def swapn(num):
    """Swaps nibbles."""
    num = num % 256
    nibh = num / 16
    nibl = num % 16
    num = nibl * 16 + nibh
    return num

def wilddenjuu(num):
    n = -1
    if num < 0 or num > 255:
        n = -1
    elif num < 25:
        n = 4
    elif num < 76:
        n = 3
    elif num < 152:
        n = 2
    else:
        n = 1
    return n

seed1=0
seed2=0

while True:
    sec=time.time()
    frame=int(sec % (256.0/60) * 60)
    #print "Seconds =", sec
    print "Frame =", frame
    frameadj = (frame*256) + ((int(((swapn(frame)+1)%256)/2)+135)%256)
    #print "frameadj =", frameadj
    seedadj = seed1*256+seed2
    #print "seedadj =", seedadj
    seed1 = ((frameadj+seedadj)%256)
    print "Seed 1 =", seed1
    seed2 = (int(((frameadj+seedadj) % 65536)/256)) ^ ((frameadj+seedadj) % 256)
    print "Seed 2 =", seed2
    seed=(seed1+seed2) % 256
    print "Random number =", seed
    wild_denjuu = wilddenjuu(seed)
    print "Wild Denjuu: #{0}".format(wild_denjuu)
    raw_input()

