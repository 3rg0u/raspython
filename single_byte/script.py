import time
import sys
import os
from colorama import init, Cursor

#In so a tai toa do x,y danh ra 9 cho
def PrintXY(x,y,a):
    sys.stdout.write(Cursor.POS(x,y))
    sys.stdout.write(" " * 9 + f"{a:08b}")
    sys.stdout.flush()

#In so a tai toa do x,y voi dinh dang b cho, tu dien day bang so 0 ben trai
def PrintXYb(x,y,a,b):
    sys.stdout.write(Cursor.POS(x,y))
    sys.stdout.write(bin(a)[2:].zfill(b))
    sys.stdout.flush()


#cuon bit cua a sang phai n lan kem hien thi tai toa do co dinh
def CuonPhai(a,n):
    PrintXY(40,2,a)
    time.sleep(1)
    for i in range(n):
        b = a<<7 & 0xFF
        a = b | (a>>1)
        PrintXY(40,2,a)
        time.sleep(1)

#cuon bit cua a sang trai n lan kem hien thi tai toa do co dinh
def CuonTrai(a,n):
    PrintXY(40,2,a)
    time.sleep(1)
    for i in range(n):
        b = a>>7 & 0x1
        a = b | (a<<1) & 0xFF
        PrintXY(40,2,a)
        time.sleep(1)

#xoa dan a tu trai qua phai
def XoaDanTuTrai(a):
    PrintXY(40,2,a)
    time.sleep(1)
    b=255 #Mat na de xoa bit (1111 1111)
    for i in range(7):
        b=b>>1 & 0xFF # thay doi mat na, them dan so 0 ben trai
        a = a & b #and voi mat na de xoa cac bi ai vi tri bit mat na = 0
        PrintXY(40,2,a)
        time.sleep(1)
    return a

#Tao hieu ung 2 so 1 chay nguoc chieu tren day 8 bit
def Sim(n, b):
    st = int(b/2-1)
    # Khoi tao mat na b bit 1
    mn = 1
    for i in (range(b-1)):
        mn = mn<<1 | 1
    #Lap n lan dieu khen bi dich chuyen
    for k in range(n):
        #tu trong ra
        m1 = 1 << st
        m2 = m1 << 1
        a= m1 | m2
        PrintXYb(40,3,a,b)
        time.sleep(1)
        for i in range(st):
            m1=m1>>1
            m2=m2<<1 & mn
            a= m1 | m2
            PrintXYb(40,3,a,b)
            time.sleep(1)

        #in gia tri 0
        PrintXYb(40,3,0,b)
        time.sleep(1)

        #tu ngoai vao
        m1 = 1
        m2 = 1 << (b-1)
        a= m1 | m2
        PrintXYb(40,3,a,b)
        time.sleep(1)
        for i in range(st):
            m1=m1<<1
            m2=m2>>1
            a= m1 | m2
            PrintXYb(40,3,a,b)
            time.sleep(1)

#Bat dau chuong trinh chinh

os.system('cls') # Xoa man hinh
a = int(input('nhap so nguyen 1 byte:'))
a=XoaDanTuTrai(a) # xoa dan ben trai
Sim(20,12) #tao hieu ung chuyen dong 2 bit 1 tu giua ra 2 ben va dao chieu
a=123
CuonPhai(a,16) #Minh hoa cuon phai a n 16 lan
CuonTrai(a,16) #Minh hoa cuon trai a n 16 lan