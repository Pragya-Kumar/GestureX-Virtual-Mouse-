
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import speech_recognition as sr
import threading
import pyautogui
import os
import win32api
import win32con
import keyboard
import mouse
import screen

# Camera settings
wCam, hCam = 640, 480
frameR = 100  # Boundary reduction for cursor movement
smoothening = 7

# Previous and current locations for smooth cursor movement
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
exit_flag = False
keyboard_open = False
calculator_open = False

# Voice input
def voice_command_listener():
    global exit_flag, keyboard_open, calculator_open
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while not exit_flag:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for commands...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                command = recognizer.recognize_google(audio).lower()
                if "exit" in command or "quit" in command:
                    print("Exit command received!")
                    exit_flag = True
                elif "keyboard" in command or "virtual keyboard" in command:
                    if not keyboard_open:
                        print("Opening virtual keyboard...")
                        os.system("osk")
                        keyboard_open = True
                elif "calculator" in command:
                    if not calculator_open:
                        print("Opening calculator...")
                        os.system("calc")
                        calculator_open = True
                
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Speech recognition service error.")
        except sr.WaitTimeoutError:
            pass

# Start voice command listener in a separate thread
threading.Thread(target=voice_command_listener, daemon=True).start()

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while not exit_flag:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)  # , flipHands=True)    Flip for left hand support

    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        x_thumb, y_thumb = lmList[4][1:]  # Thumb tip
        
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Move cursor only if thumb is not stretched
        if fingers[0] == 0:
            if fingers[1] == 1 and fingers[2] == 1:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

        # Left Click: Index Finger Folded
        if fingers[1] == 0 and fingers[2] == 1:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            cv2.putText(img, "Left Click", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Right Click: Middle Finger Folded
        if fingers[1] == 1 and fingers[2] == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            cv2.putText(img, "Right Click", (x2, y2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        # Double Click: No gap between index and middle finger
        distance = abs(x1 - x2) + abs(y1 - y2)
        if fingers[1] == 1 and fingers[2] == 1 and distance < 20:
            autopy.mouse.click()
            autopy.mouse.click()
            cv2.putText(img, "Double Click", (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
        # Scrolling: Only Thumb is Out & Direction-Based
        if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
            if y_thumb < lmList[3][2]:  # Thumb pointing up
                pyautogui.scroll(10)
            else:  # Thumb pointing down
                pyautogui.scroll(-10)
                
        # Virtual Keyboard Input to Notepad
        if keyboard_open and fingers[1] == 1 and all(f == 0 for f in fingers[2:]):
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.typewrite("a")  # Simulating dynamic keypress
            print("Key Pressed: a")

    # Frame Rate Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q') or exit_flag:
        break

cap.release()
cv2.destroyAllWindows()

