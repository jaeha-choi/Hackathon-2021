# PROJECT COCONUTS

Github repo: https://github.com/jaeha-choi/Hackathon-2021

### Objectives
- Share files between devices easily.
- Sends the clipboard content. (Only in LAN unless using heartbeat packets. Mobile devices may not support heartbeat too well)
- End-to-end encryption setting for enhanced security.
- Optional: Support all functionalities in WAN
- Optional: Tcp hole punching or uses central server if user desires (for enhancing privacy)

### Supported Operating Systems
- Desktop: Windows/macOS/Linux 
- Mobile: Android/iOS

### Dependencies:
- `Python`: Base language for server / desktop clients
- `Flutter`: Used for android/iOS apps
- `PyQt==5.15.4`: Used for client GUI
- `pyperclip==1.8.2`: Used for clipboard
- `qdarkstyle==3.0.2`: Used for dark mode on desktop client

## **GUI Requirements**

### All Versions
1. "Clipboard send"  button: Clicking the button will broadcast the clipboard content to all devices
2. "File picker" button: Picks a file. Should support multiple file selection
3. "Send" button: Sends the file.
4. "Host" field: A text field to enter host (or unique ID) 
5. "Host" label: A distinctive label that shows current device's host (or unique ID)
A. Optional: Support dark mode + button to trigger it

### Desktop
- A. Optional: Minimize to tray.
- B. Optional: Drag and drop support
- C. Optional: Key binding (aka shortcut) support

<img width="847" alt="image" src="https://user-images.githubusercontent.com/62778661/114319405-48c4ef00-9ac6-11eb-88c9-0f2609928a5c.png">


### Mobile
1. "Photo picker" button: Picks images and videos by opening the gallery.

## **Functional Requirements**

### Client
1. When the app opens, initial packet will be sent to the server for hole punching
2. If hole punching is successful (need to decide how to determine successful state), standby and send heartbeat every few min
3. If hole punching is unsuccessful, notify user that central server is going to be used for transferring data.

### Server
1. Relay Server: Stores basic information about the host including the following:
```
    - UUID (some portion will be used by the peer to connect)
    - Public IP
    - Port
    - Private IP (could be unnecessary)
```
2. Central Server: Transfer data via central server if hole punching was unsuccessful.
