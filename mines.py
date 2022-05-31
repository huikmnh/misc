import pyautogui
from PIL import Image
import numpy as np
import PIL
import time

def screenshot():
    time.sleep(0.02)
    pyautogui.moveTo(100, 200)
    # return pyautogui.screenshot()
    im = PIL.ImageGrab.grab(bbox=(x3, y3, x4, y4))
    return im

# def diff(a, b):
#     x1, y1, z1 = a
#     x2, y2, z2 = b
#     return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2)

ref = [137, 240, 172]
# r= 10

# def check(arr, row, col):
#     for i in range(r):
#         for j in range(r):
#             if arr[row+i,col+j,0] != 128:
#                 return False
#     return True

# def my_change(arr):
#     arr = arr.astype('int32')
#     rows = arr.sum(axis=(1,2))
#     y = []
#     for row in range(len(rows)-1):
#         if rows[row+1] - rows[row] > 350000:
#             y.append(row)
#     cols = arr.sum(axis=(0,2))
#     dy = (y[-1] - y[0])/(len(y))
#     x = []
#     for col in range(len(cols)-1):
#         if cols[col+1] - cols[col] > 350000:
#             x.append(col)
#     dx = (x[-1] - x[0])/(len(x))
#     return y, x, dy, dx

ddd = {}

def my_change_2(arr):
    arr = arr.astype('int32')
    rows = arr.sum(axis=(1))
    im2 = PIL.Image.fromarray(np.uint8(arr))
    im2.show()
    y = []
    for row in range(len(rows)-1):
        if rows[row+1] - rows[row] > 450000/6:
            y.append(row)
    cols = arr.sum(axis=(0))
    # print(cols[400:600])
    dy = (y[-1] - y[0])/(len(y))
    x = []
    cols = [i if i > 300000/6 else 0 for i in cols]
    ddd[0] = cols
    for col in range(len(cols)-1):
        if cols[col+1] - cols[col] > 350000/6:
            x.append(col)
    try:
        dx = (x[-1] - x[0])/(len(x))
    except:
        dx = 99
    return y, x, dy, dx

def ana_im(im):
    I = np.asarray(im)
    I.setflags(write=1)
    I3 = I.copy().astype('int32')
    I4 = I3.copy()
    I3[:,:,] = ref
    I5 = I4 - I3
    I5 = I5 * I5
    I5 = I5.sum(axis=2)
    I6 = I5.copy()
    I6 = np.where(I5 < 20000, 128, 0)    
    rows, cols, _ = I.shape
    kernel = 10, 10
    sub_rows, sub_cols = rows - kernel[0], cols - kernel[1]
    I7 = I6[0:sub_rows, 0:sub_cols].copy()
    for y in range(kernel[0]):
        for x in range(kernel[1]):
#             print(x,y)
            I7 = I7 & I6[y:y+sub_rows, x:x+sub_cols] 
    return my_change_2(I7)

# im = Image.open('mines.png')
# im = screenshot()
# a = ana_im(im)

xx = [205, 255, 305, 355, 405, 455, 505, 553, 603, 653, 703, 753, 803, 853, 903, 953, 1001, 1051, 1101, 1151, 1201, 1251, 1301, 1351, 1401, 1449, 1499, 1549, 1599, 1649]
yy = [313, 363, 413, 463, 513, 561, 611, 661, 711, 761, 811, 861, 911, 961, 1009, 1059]
dx = 48.13333333333333
dy = 46.625

x3, y3, x4, y4 = 200, 300, 1750, 1150

xx3 = [i for i in xx]
yy3 = [i for i in yy] 

xx = [i - x3 for i in xx]
yy = [i - y3 for i in yy] 

# yy, xx, dy, dx = ana_im(im)
dy_0, dy_1, dx_0, dx_1 = int(dy*0.2), int(dy*0.8), int(dx*0.2), int(dx*0.8)
print(yy, xx, dy, dx, len(yy), len(xx))

m = {
    0:[245.41995074, 245.42857143, 245.42857143],
    1:[218.13669951, 236.22660099, 240.10344828],
    2:[218.97536946, 224.2635468,  205.96305419],
    3:[235.36206897, 206.18226601, 217.59605911],
    4:[202.88054187, 213.17857143, 232.16133005],
    5:[229.61576355, 205.40517241, 205.40517241],
    6:[198.36699507, 219.54187192, 203.55172414],
    7:[225.68965517, 212.87561576, 225.69458128],
    9:[228.21182266, 170.71305419,  64.07758621],  # flaged
    11:[115.73275862, 199.08374384, 255.]          # unkown
}

def get_digit(arr):
    x, y, z = arr.mean(axis=(0,1))
    min = 10000
    ret = 99
    for k, v in m.items():
        x2, y2, z2 = v
        x2, y2, z2 = x2-x, y2-y, z2-z
        s = x2*x2 + y2*y2 + z2*z2
        if s < min:
            min = s
            ret = k
    return ret

def get_mat(arr):
    rows, cols = len(yy),len(xx)
    ret = np.ones([rows, cols],dtype='int32')
    for x in range(cols):
        for y in range(rows):
            I8 = arr[yy[y]+dy_0:yy[y]+dy_1, xx[x]+dx_0:xx[x]+dx_1]
            d = get_digit(I8)
            # if x == 10 and y == 10:
                # print(x, y, d)
                # im2 = PIL.Image.fromarray(np.uint8(I8))
                # im2.show()
            ret[y,x] = d
    return ret

def init():
    ddd[1] = np.full([rows, cols], -1, dtype='int32')
    left_c(ddd[1], 4, 4)
    ddd[2] = set()

def get_mat_2(arr):
    rows, cols = len(yy),len(xx)
    # ret = np.ones([rows, cols],dtype='int32')
    ret = ddd[1]
    for x in range(cols):
        for y in range(rows):
            v = ret[y, x]
            if v < 0 or v == 11:
                I8 = arr[yy[y]+dy_0:yy[y]+dy_1, xx[x]+dx_0:xx[x]+dx_1]
                d = get_digit(I8)
                # if x == 10 and y == 10:
                    # print(x, y, d)
                    # im2 = PIL.Image.fromarray(np.uint8(I8))
                    # im2.show()
                ret[y,x] = d
    return ret


rows, cols = len(yy),len(xx)

def around_count(mat, row, col):
    ret = 0
    f_cnt = 0
    for ddy in (-1,0,1):
        for ddx in (-1, 0, 1):
            y, x = ddy+row, ddx+col
            if x >= 0 and x < cols and y >= 0 and y < rows:
                if mat[y, x] > 8:
                    ret += 1
                if mat[y, x] == 9:
                    f_cnt += 1
    if ret == f_cnt:
        my_v = mat[row, col]
        if my_v == f_cnt:
            # print("add skip item")
            ddd[2].add((row, col))
    return ret

def flag_around(mat, row, col):
    ret = 0
    for ddy in (-1,0,1):
        for ddx in (-1, 0, 1):
            y, x = ddy+row, ddx+col
            if x >= 0 and x < cols and y >= 0 and y < rows:
                if mat[y, x] == 11:
                    # print('flag', y, x)
                    # print(xx[x]+int(dx/2), yy[y]+int(dy/2), xx[x], int(dx/2), yy[y], int(dy/2))
                    # pyautogui.rightClick(x=xx[x]+int(dx/2), y=yy[y]+int(dy/2))
                    # mat[y, x] = 9
                    right_c(mat, x, y)
                    ret += 1
    return ret

def right_c(mat, x, y):
    pyautogui.rightClick(x=xx3[x]+int(dx/2), y=yy3[y]+int(dy/2))
    mat[y, x] = 9

def middle_c(mat, x, y):
    pyautogui.middleClick(x=xx3[x]+int(dx/2), y=yy3[y]+int(dy/2))

def left_c(mat, x, y):
    pyautogui.leftClick(x=xx3[x]+int(dx/2), y=yy3[y]+int(dy/2))


##########################################################################

import ctypes

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]





def move_to(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x*1280//65536, y*800//65536, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



def move_to2(x, y):
    # print('x, y', x, y)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x*65536//1280//2, y*65536//800//2, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

val_map = {
    'L':(0x2, 0x4),
    "M":(0x20, 0x40),
    "R":(0x8, 0x10)
}

def click_bu(k):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, val_map[k][0], 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    ii_.mi = MouseInput(0, 0, 0, val_map[k][1], 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    # time.sleep(0.05)


def right_c(mat, x, y):
    move_to2(xx3[x]+int(dx/2), yy3[y]+int(dy/2))
    click_bu('R')
    mat[y, x] = 9

def middle_c(mat, x, y):
    move_to2(xx3[x]+int(dx/2), yy3[y]+int(dy/2))
    click_bu('M')

def left_c(mat, x, y):
    move_to2(xx3[x]+int(dx/2), yy3[y]+int(dy/2))
    click_bu('L')



########################################################



def s1(mat):
    ret = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) in ddd[2]:
                # print('skip')
                continue
            v = mat[row, col]
            if  v > 0 and v < 9:
                if around_count(mat, row, col) == v:
                    ret += flag_around(mat, row, col)
            elif v == 0:
                ddd[2].add((row, col))
    return ret

def flag_count(mat, row, col):
    flag_cnt, unkown_cnt = 0, 0
    for ddy in (-1,0,1):
        for ddx in (-1, 0, 1):
            y, x = ddy+row, ddx+col
            if x >= 0 and x < cols and y >= 0 and y < rows:
                if mat[y, x] == 9:
                    flag_cnt += 1
                if mat[y, x] == 11:
                    unkown_cnt += 1
    return flag_cnt, unkown_cnt


def clear_mine(mat, row, col):
    for ddy in (-1,0,1):
        for ddx in (-1, 0, 1):
            y, x = ddy+row, ddx+col
            if x >= 0 and x < cols and y >= 0 and y < rows:
                if mat[y, x] == 11:
                    left_c(mat, x, y)

def s2(mat):
    ret = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) in ddd[2]:
                # print('skip')
                continue
            v = mat[row, col]
            if  v > 0 and v < 9:
                flag_cnt, unkown_cnt = flag_count(mat, row, col)
                if v == flag_cnt and unkown_cnt:
                    ret += 1
                    middle_c(mat, col, row)
                    # mat = deal_screen()
                    # clear_mine(mat, row, col)
    return ret

def around_set(mat, row, col):
    ret = set()
    for ddy in (-1,0,1):
        for ddx in (-1, 0, 1):
            y, x = ddy+row, ddx+col
            if x >= 0 and x < cols and y >= 0 and y < rows:
                if mat[y, x] == 11:
                    ret.add(y*256+x)
    return ret

def s3(mat):
    for row in range(rows):
        for col in range(cols):
            v = mat[row, col]
            if  v > 0 and v < 9:
                # print("s3 go x y", col, row)
                my_set = around_set(mat, row, col)
                if my_set:
                    for ddy in (-2, -1, 0, 1, 2):
                        for ddx in (-2, -1, 0, 1, 2):
                            y, x = ddy+row, ddx+col
                            if x >= 0 and x < cols and y >= 0 and y < rows:
                                v_2 = mat[y, x]
                                if v_2 ==v and v_2 > 0 and v_2 < 9:
                                    set_2 = around_set(mat, y, x)
                                    if my_set.issubset(set_2) and not set_2.issubset(my_set):
                                        a = set_2 - my_set
                                        for aa in a:
                                            y_2 = aa // 256
                                            x_2 = aa % 256
                                            print("safe x %d y %d"%(x_2, y_2), my_set, set_2, a)
                                            left_c(mat, x_2, y_2)

def around_set_ex(mat, row, col):
    un_set = set()
    f_set = set()
    for ddy in (-1,0,1):
        for ddx in (-1, 0, 1):
            y, x = ddy+row, ddx+col
            if x >= 0 and x < cols and y >= 0 and y < rows:
                if mat[y, x] == 11:
                    un_set.add(y*256+x)
                if mat[y, x] == 9:
                    f_set.add(y*256+x)
    return un_set, f_set

def sub_4(mat, row, col):
    ret = 0
    v = mat[row, col]
    if  v > 0 and v < 9:
        # print("sub_4 go x y", col, row)
        my_set, f_my_set = around_set_ex(mat, row, col)
        my_un = v - len(f_my_set)
        if my_set:
            for ddy in (-2, -1, 0, 1, 2):
                for ddx in (-2, -1, 0, 1, 2):
                    y, x = ddy+row, ddx+col
                    if x >= 0 and x < cols and y >= 0 and y < rows:
                        v_2 = mat[y, x]
                        if v_2 > 0 and v_2 < 9:
                            un_set_2, f_set_2 = around_set_ex(mat, y, x)
                            un_2 = v_2 - len(f_set_2)
                            if my_set.issubset(un_set_2) and not un_set_2.issubset(my_set):
                                a = un_set_2 - my_set
                                if my_un == un_2:
                                    for aa in a:
                                        y_2 = aa // 256
                                        x_2 = aa % 256
                                        print("safe x_2 %d y_2 %d"%(x_2, y_2), my_set, un_set_2, a, "center x, y %d %d"%(x, y))
                                        left_c(mat, x_2, y_2)
                                        ret += 1
                                if un_2 - my_un == len(a):
                                    for aa in a:
                                        y_2 = aa // 256
                                        x_2 = aa % 256
                                        print("flag x_2 %d y_2 %d"%(x_2, y_2), my_set, un_set_2, a, "center x, y %d %d"%(x, y))
                                        right_c(mat, x_2, y_2)
                                        ret += 1
                            if ret:
                                return ret
                            a = un_set_2 - my_set
                            if un_2 - my_un == len(a):
                                for aa in a:
                                    y_2 = aa // 256
                                    x_2 = aa % 256
                                    print("flag x_2 %d y_2 %d"%(x_2, y_2), my_set, un_set_2, a, "center x, y %d %d"%(x, y))
                                    right_c(mat, x_2, y_2)
                                    ret += 1
    return ret                   
                            # if my_set.issubset(un_set_2) and not un_set_2.issubset(my_set) and v == v_2 - len(f_set_2) and not f_my_set:
                            #     a = un_set_2 - my_set
                            #     for aa in a:
                            #         y_2 = aa // 256
                            #         x_2 = aa % 256
                            #         print("safe x_2 %d y_2 %d"%(x_2, y_2), my_set, un_set_2, a, "center x, y %d %d"%(x, y))
                                    # left_c(mat, x_2, y_2)   

def s4(mat):
    ret = 0
    for row in range(rows):
        for col in range(cols):
            v = mat[row, col]
            if  v > 0 and v < 9:
                ret += sub_4(mat, row, col)
    return ret

def do():
    while True:
        n = 0
        a = deal_screen()
        n += s1(a)
        n += s2(a)
        if not n:
            break

def do2():
    while True:
        while True:
            n = 0
            a = deal_screen()
            n += s1(a)
            n += s2(a)
            if not n:
                print('b12')
                break
        n4 = s4(deal_screen())
        if n4:
            continue
        else:
            break

import code
def deal_screen():
    print('=====>')
    i1 = screenshot()
    I1 = np.asarray(i1)
    while True:
        im = screenshot()
        # im = PIL.ImageGrab.grab(bbox=(200, 300, 1750, 1150))
        I = np.asarray(im)
        I.setflags(write=1)
        di = I - I1
        if np.all( di == 0):
            return get_mat_2(I)
        else:
            # code.interact(local=locals())
            I1 = I
    # print(mat)
    # return mat

go = deal_screen
# print(a)

def start():
    while True:
        input()
        init()
        do2()
        pyautogui.moveTo(400, 200)

start()

init()
a = go()

import time
def test_time():
    start = time.time()
    for row in range(rows):
        for col in range(cols):
            left_c(a, col+300, row+300)
    end = time.time()
    print("time use %f"%(end-start))

import code
code.interact(local=locals())

















# mouse_button_down_mapping = {
#     MouseButton.LEFT.name: 0x0002,
#     MouseButton.MIDDLE.name: 0x0020,
#     MouseButton.RIGHT.name: 0x0008
# }

# mouse_button_up_mapping = {
#     MouseButton.LEFT.name: 0x0004,
#     MouseButton.MIDDLE.name: 0x0040,
#     MouseButton.RIGHT.name: 0x0010
# }



import ctypes

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]





def move_to(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x*1280//65536, y*800//65536, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



def move_to2(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x*65536//1280, y*65536//800, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

val_map = {
    'L':(0x2, 0x4),
    "M":(0x20, 0x40),
    "R":(0x8, 0x10)
}

def click_bu(k):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, val_map[k][0], 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    ii_.mi = MouseInput(0, 0, 0, val_map[k][1], 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def right_c(mat, x, y):
    move_to2(x, y)
    click_bu('R')
    mat[y, x] = 9

def middle_c(mat, x, y):
    move_to2(x, y)
    click_bu('M')

def left_c(mat, x, y):
    move_to2(x, y)
    click_bu('L')

