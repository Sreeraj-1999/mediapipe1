import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
import pygame


pygame.mixer.init()

video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]

scored_animation_timer = 0
scored_animation_duration = 2  

pygame.mixer.music.load("C:\\Users\\SREERAJ\\Downloads\\x2downloadapp-aqua-lollipop-candyman-128-kbps_ROSQ7Oyz.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

while True:
    imgBG = cv2.imread(r"D:\DL projects March\snake\newgame\BG.png")
    success, img = video.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:477]

    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 3)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    computerMove = random.randint(1, 3)  

                    imgAI = cv2.imread(f'newgame/{computerMove}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    if (playerMove == 1 and computerMove == 3) or (playerMove == 2 and computerMove == 1) or (
                            playerMove == 3 and computerMove == 2):
                        scores[1] += 1  
                        scored_animation_timer = time.time()  
                    if (playerMove == 3 and computerMove == 1) or (playerMove == 1 and computerMove == 2) or (
                            playerMove == 2 and computerMove == 3):
                        scores[0] += 1  
                        

    imgBG[234:654, 796:1193] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str((scores[0])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 4)
    cv2.putText(imgBG, str((scores[1])), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 4)

    
    if scored_animation_timer > 0:
        cv2.putText(imgBG, "GO CHAMP!", (300, 300), cv2.FONT_HERSHEY_DUPLEX, 4, (0, 0, 255), 5)
        if time.time() - scored_animation_timer > scored_animation_duration:
            scored_animation_timer = 0

    cv2.imshow("bg", imgBG)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    if key == ord('q'):
        break


pygame.mixer.music.stop()
pygame.quit()

video.release()
cv2.destroyAllWindows()
