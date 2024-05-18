import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame
import os

pygame.init()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cv2.namedWindow("Image")
cv2.moveWindow("Image", 0, 0)

# Importing all images
imgtennisCourt = cv2.imread("Resources/Pixel Art Desert Seamless Background_ Stock Vector - Illustration of colorful, cute_ 96712971.jpeg")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgEndPhoto = []
imgEndPhotoFolderName = 'gameEndPhoto'
for filename in os.listdir(imgEndPhotoFolderName):
    f = os.path.join(imgEndPhotoFolderName, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        imgEndPhoto.append(cv2.imread(f))

imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (70, 70))
imgBat1 = cv2.resize(cv2.imread("Resources/leftPat.png", cv2.IMREAD_UNCHANGED), (50,150))
imgBat2 = cv2.resize(cv2.imread("Resources/rightPat.png", cv2.IMREAD_UNCHANGED),(50,150))

# Load music effects
pygame.mixer.music.load('sound/gameStartMusic.mp3')
leftsound = pygame.mixer.Sound('sound/leftsound.wav')
rightsound = pygame.mixer.Sound('sound/rightsound.wav')

# Play music effect
pygame.mixer.music.play(-1, 0.0, 0)
pygame.time.delay(2000)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]
gameOverSoundPlayed = False  # Flag to track if game over sound has been played
one_player = False
two_player = False


def show_login_page():
    global one_player, two_player, img
    while not (one_player or two_player):
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
        blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
        img = blended_img

        hands, img = detector.findHands(img, flipType=False)

        # Define button regions
        button1_pos = (490, 270, 790, 320)  # (x1, y1, x2, y2)
        button2_pos = (490, 370, 790, 420)  # (x1, y1, x2, y2)

        # Draw buttons
        cv2.rectangle(img, (button1_pos[0], button1_pos[1]), (button1_pos[2], button1_pos[3]), (0, 0, 255), -1)
        cv2.rectangle(img, (button2_pos[0], button2_pos[1]), (button2_pos[2], button2_pos[3]), (0, 0, 255), -1)

        cv2.putText(img, "1 Player", (button1_pos[0] + 30, button1_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, "2 Players", (button2_pos[0] + 30, button2_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()

        # Check for mouse click
        def mouse_click(event, x, y, flags, param):
            global one_player, two_player
            if event == cv2.EVENT_LBUTTONDOWN:
                if button1_pos[0] <= x <= button1_pos[2] and button1_pos[1] <= y <= button1_pos[3]:
                    one_player = True
                elif button2_pos[0] <= x <= button2_pos[2] and button2_pos[1] <= y <= button2_pos[3]:
                    two_player = True

        cv2.setMouseCallback("Image", mouse_click)


show_login_page()

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw

    # Overlaying the background image
    imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
    blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
    img = blended_img

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if one_player:
                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        leftsound.play()
                        ballPos[0] += 30
                        score[0] += 1

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        rightsound.play()
                        ballPos[0] -= 30
                        score[1] += 1

            elif two_player:
                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        leftsound.play()
                        ballPos[0] += 30
                        score[0] += 1

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        rightsound.play()
                        ballPos[0] -= 30
                        score[1] += 1

    # Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

        # Load gameOver music (only if it hasn't been played before)
        if not gameOverSoundPlayed:
            pygame.time.delay(1000)
            gameOverSound = pygame.mixer.Sound('sound/gameOverSound.wav')
            gameOverSound.play()
            pygame.mixer.music.stop()
            gameOverSoundPlayed = True

    if gameOver:
        img = imgEndPhoto[random.randrange(len(imgEndPhoto))]
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)
        cv2.imshow("Image", img)
        cv2.waitKey(2000)  # Show game end photo for 10 seconds

        img = imgGameOver.copy()
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)
        cv2.imshow("Image", img)
        cv2.waitKey(3000)  # Show game over screen for 3 seconds

        one_player = False
        two_player = False
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        gameOverSoundPlayed = False  # Reset the flag
        pygame.mixer.music.play(-1)
        show_login_page()
    else:
        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        # cv2.imshow("aaaimg", img)
        # cv2.imshow("aaaimgBall", imgBall)
        # cv2.waitKey(0)
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        # Draw the scores
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        # Display
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        if key == 27:  # ESC key
            break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
