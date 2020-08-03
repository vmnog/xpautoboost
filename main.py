import ctypes
from ctypes import wintypes
from python_imagesearch.imagesearch import imagesearch_loop, imagesearch
from pyautogui import moveTo, click, typewrite, position, press, doubleClick
import time


user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)   # Alt
    PressKey(VK_TAB)    # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU) # Alt~

# Starting a match
def startMatch():
    # Searching for play button
    pos = imagesearch_loop("./images/btn_play.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

    # Searching for coop button
    pos = imagesearch_loop("./images/coop_match.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

    # Searching for confirm button
    pos = imagesearch_loop("./images/btn_confirm.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

    # Getting in queue
    pos = imagesearch_loop("./images/btn_findmatch.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

    # Accept found queue
    pos = imagesearch_loop("./images/btn_accept.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

# Looks for a champion and selects it
def selectChampion():
   
    for x in range(3):
        # Searchs for Yuumi
        pos = imagesearch("./images/search_champion.png")

        if pos[0] != -1:    
            print("im gonna pick yuumi")
            moveTo(pos[0], pos[1])
            click()    
        
            time.sleep(2)
            
            # Type yuumi
            typewrite('Soraka')

            time.sleep(5)

            # Select Yuumi
            #pos = imagesearch_loop("./images/yuumi_face.png", 1)
            
            #moveTo(pos[0], pos[1])
            
            moveTo(700,332)
            time.sleep(5)

            click()

            time.sleep(2)

            # Confirm the champion select
            pos = imagesearch_loop("./images/confirm_champion.png", 1)
            
            moveTo(pos[0], pos[1])

            time.sleep(5)

            click()
            print("champion selected")
            print("awaiting 2 minutes before start playing yuumi")
            time.sleep(200)

            playsYuumi()
        else:
            print("button accepted")

            time.sleep(20) # in case clients is slow or someone dodge the queue

            # if someone dodges the queue the bot still on queue
            # Accept found queue
            pos = imagesearch("./images/btn_accept.png")
            if pos[0] != -1:    
                moveTo(pos[0], pos[1])
                click() 
                print("match accepted again")
                time.sleep(10)

                selectChampion()
            else:
                selectChampion()

def playsYuumi():

    # Q = 0x51 W = 0x5eqw7 E = 0x45  R = 0x52  D = 0x44 F = 0x46 CTRL = 0x11  4 = 0x34
    alieds = [
        [1487,709],
        [1538,709],
        [1598,709],
        [1650,709]
    ]

    for alied in alieds: 

        moveTo(985,494) #middle of screen
        click()

        moveTo(alied[0], alied[1])
        click()  

        # Press CTRL + W
        PressKey(0x11)
        PressKey(0x57)
        ReleaseKey(0x57)
        ReleaseKey(0x11)

        # Press CTRL + E
        PressKey(0x11)
        PressKey(0x45)
        ReleaseKey(0x45)
        ReleaseKey(0x11)    

        # Press CTRL + Q
        PressKey(0x11)
        PressKey(0x51)
        ReleaseKey(0x51)
        ReleaseKey(0x11)
      
        # Press CTRL + R
        PressKey(0x11)
        PressKey(0x52)
        ReleaseKey(0x52)
        ReleaseKey(0x11)

        PressKey(0x57) # Press W
        ReleaseKey(0x57)

        time.sleep(30)

        PressKey(0x45) # Press E
        ReleaseKey(0x45)

       	PressKey(0x51) # Press Q
        ReleaseKey(0x51)

        PressKey(0x52) # Press R
        ReleaseKey(0x52)

        PressKey(0x44) # Press D
        ReleaseKey(0x44)

        PressKey(0x46) # Press F
        ReleaseKey(0x46)
        
        PressKey(0x34) # Press 4
        ReleaseKey(0x34)
        
	
    PressKey(0x42) # Press B
    ReleaseKey(0x42)

    time.sleep(10)
	      

    # try to find btn_choose_champion_ok.png
    # if found move and click on [916,574]
    # then try to find btn_choose_champion_ok_enabled.png
    pos = imagesearch("./images/btn_choose_champion_ok.png")
    if pos[0] != -1:
        # achou o botao playagain
        print("Choose champion to select")
        moveTo(916,574)
        click()
        
        # after choosing a champion click in OK
        pos = imagesearch("./images/btn_choose_champion_ok_enabled.png")
        moveTo(pos[0], pos[1])
        click()

        time.sleep(3)
        
        # try to find play again button
        pos = imagesearch("./images/btn_playagain.png")
        if pos[0] != -1:
            # achou o botao playagain
            print("play again button found")
            playAgain()

    else:
        # try to find play again button
        pos = imagesearch("./images/btn_playagain.png")
        if pos[0] != -1:
            # achou o botao playagain
            print("play again button found")
            playAgain()
        else:
            # nao achou botao playagain
            pos = imagesearch("./images/btn_oklvlup.png")
            if pos[0] != -1:
                print("found ok button")
                moveTo(pos[0], pos[1])
                click()

                time.sleep(5)
                print("accepted ok, now lets play again")
                playAgain()
            else:
                # se nao achou playagain nem okbutton entao continua jogando de yuumi
                print("playing yuumi again")
                playsYuumi()
        

def playAgain():

    # Getting in queue
    pos = imagesearch_loop("./images/btn_playagain.png", 1)
    
    moveTo(pos[0], pos[1])
    click()


    # Getting in queue
    pos = imagesearch_loop("./images/btn_findmatch.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

    # Accept found queue
    pos = imagesearch_loop("./images/btn_accept.png", 1)
    
    moveTo(pos[0], pos[1])
    click()

    selectChampion()

    playsYuumi()

if __name__ == "__main__" :
        #startMatch()
        #selectChampion()
        #playAgain()
        #playsYuumi()
        #print(position())
        print("==================================")
        option = input("1 - Just Play\n\n2 - Start Match")
        print("==================================")
        if(option=="1"):
            playsYuumi()
        else:
            startMatch()
            selectChampion()
            playsYuumi()
