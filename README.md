
# GestureX – A Virtual Mouse

GestureX is a hand-gesture controlled virtual mouse built using **MediaPipe** and a custom **HandTrackingModule**.  
It lets you control your computer without touching the mouse by recognizing real-time finger positions and translating them into system actions.

This project focuses on smooth cursor control, intuitive gesture detection, and basic voice-activated commands.

## Features
### Cursor Control
- **Move Cursor:** Use **two fingers up** (index + middle).  
  The cursor follows your hand smoothly based on detected landmarks.
- **Freeze Cursor:** Keep **thumb out** to stop the cursor from moving.

### Mouse Actions
- **Left Click:** Index finger folded.  
- **Right Click:** Middle finger folded.  
- **Double Click:** No gap between index and middle finger.

### Scrolling
- Only **thumb out**  
- System scrolls **up or down** based on hand direction.

### Voice Commands
Built-in command listener for:
- Opening the **On-Screen Keyboard**
- Opening the **Calculator**


## Understanding MediaPipe Hand Tracking

GestureX uses MediaPipe Hands, a real-time ML model from Google that identifies 21 hand landmarks.
These points help the system understand finger positions, bending angles, distances, and hand movement.
Using this information, GestureX can detect gestures for cursor control, clicking, scrolling, and voice-triggered actions.

## Hand Landmark Diagram

![MediaPipe Hand Landmarks](./assets/hand-landmarks.png)

## How It Works
The hand landmarks detected by MediaPipe provide the core data used for gesture recognition. GestureX analyzes these points to determine:

- Which fingers are up or folded
- Distances and gaps between fingers
- Thumb orientation
- Overall hand movement direction
- The gestures are mapped to system actions using PyAutoGUI.

## Gesture Summary

| Action             | Gesture                         |
| ------------------ | ------------------------------- |
| **Cursor Move**    | Index + Middle Finger Up        |
| **Freeze Cursor**  | Thumb Out                       |
| **Left Click**     | Index Finger Folded             |
| **Right Click**    | Middle Finger Folded            |
| **Double Click**   | No gap between Index and Middle |
| **Scroll**         | Only Thumb Out + Move Hand      |
| **Voice Commands** | Say “Keyboard” or “Calculator”  |

## Tech Stack
- **Python**
- **MediaPipe (Google)**    
- **OpenCV**
- **HandTrackingModule** (custom utility)
- **PyAutoGUI** for mouse and keyboard actions
- **SpeechRecognition** (for voice commands)


##  Project Structure
```bash
GestureX/
├── HandTrackingModule.py
├── gesturex_virtual_mouse.py
├── requirements.txt
├── README.md
└── assets/
```
## Installation

1. **Clone the repository**

```bash
  git clone https://github.com/Pragya-Kumar/GestureX-Virtual-Mouse-.git
  cd GestureX-Virtual-Mouse-
```
2. **Install dependencies**
```bash
    pip install -r requirements.txt
```
3. **Run the Project**
```bash
    python gesturex_virtual_mouse.py
```
 
## Important Note

- This project works best with **Python 3.8**.
- Some of the required libraries like MediaPipe and PyAudio may not function properly on newer Python versions (3.10+).
- If you face installation errors, create a virtual environment using Python 3.8.

## Credits & Collaborators
This project is made possible by the efforts of:
- [Pragya Kumar](https://github.com/Pragya-Kumar)
- [Geetish Mahato](https://github.com/GeetishM) 
- [Anamika Dey](https://github.com/anamikadey099)

