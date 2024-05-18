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
imgtennisCourt = cv2.imread("Resources/peakpx.jpg")
imgGameOver = cv2.imread("Resources/newGameOver.png")
imgGameOver = cv2.resize(imgGameOver, (1280, 720))  # Resize game over image
imgEndPhoto = []
imgEndPhotoFolderName = 'fullScreenGameEndPhoto'
for filename in os.listdir(imgEndPhotoFolderName):
    f = os.path.join(imgEndPhotoFolderName, filename)
    if os.path.isfile(f):
        imgEndPhoto.append(cv2.resize(cv2.imread(f),(1280,720)))

imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (60, 60))
imgBat1 = cv2.resize(cv2.imread("Resources/leftPat.png", cv2.IMREAD_UNCHANGED), (50, 150))
imgBat2 = cv2.resize(cv2.imread("Resources/rightPat.png", cv2.IMREAD_UNCHANGED), (50, 150))

# Load music effects
pygame.mixer.music.load('sound/Kirbys Dream Land  Green Greens.mp3')
leftsound = pygame.mixer.Sound('sound/leftsound.wav')
rightsound = pygame.mixer.Sound('sound/rightsound.wav')
gameOverSound = pygame.mixer.Sound('sound/gameOverSound.wav')  # Add this line to load the game over sound

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
challenge_mode = False


def show_login_page():
    global one_player, two_player, challenge_mode, img
    while not (one_player or two_player or challenge_mode):
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
        blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
        img = blended_img

        hands, img = detector.findHands(img, flipType=False)

        # Define button regions
        button1_pos = (490, 270, 790, 320)  # (x1, y1, x2, y2)
        button2_pos = (490, 370, 790, 420)  # (x1, y1, x2, y2)
        button3_pos = (490, 470, 790, 520)  # (x1, y1, x2, y2)

        # Draw buttons
        cv2.rectangle(img, (button1_pos[0], button1_pos[1]), (button1_pos[2], button1_pos[3]), (0, 0, 255), -1)
        cv2.rectangle(img, (button2_pos[0], button2_pos[1]), (button2_pos[2], button2_pos[3]), (0, 0, 255), -1)
        cv2.rectangle(img, (button3_pos[0], button3_pos[1]), (button3_pos[2], button3_pos[3]), (0, 0, 255), -1)

        cv2.putText(img, "1 Player", (button1_pos[0] + 30, button1_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, "2 Players", (button2_pos[0] + 30, button2_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, "Challenge Mode", (button3_pos[0] + 10, button3_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
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
            global one_player, two_player, challenge_mode
            if event == cv2.EVENT_LBUTTONDOWN:
                if button1_pos[0] <= x <= button1_pos[2] and button1_pos[1] <= y <= button1_pos[3]:
                    one_player = True
                elif button2_pos[0] <= x <= button2_pos[2] and button2_pos[1] <= y <= button2_pos[3]:
                    two_player = True
                elif button3_pos[0] <= x <= button3_pos[2] and button3_pos[1] <= y <= button3_pos[3]:
                    challenge_mode = True

        cv2.setMouseCallback("Image", mouse_click)


show_login_page()

# Challenge Mode Variables
ballPos1 = [100, 100]
speedX1 = speedY1 = random.randint(10, 15)
gameOver1 = False
ballPos2 = [800, 450]
speedX2 = speedY2 = random.randint(10, 15)
gameOver2 = False

def random_speed():
    return random.randint(13, 17)

def check_ball_collision(ballPos1, ballPos2):
    dist = np.linalg.norm(np.array(ballPos1) - np.array(ballPos2))
    return dist < 50

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    hands, img = detector.findHands(img, flipType=False)  # with draw

    imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
    blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
    img = blended_img

    if challenge_mode:
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos1[0] < 59 + w1 and y1 < ballPos1[1] < y1 + h1:
                        speedX1 = -speedX1
                        speedY1 = random_speed()
                        ballPos1[0] += 30
                        score[0] += 1
                        leftsound.play()

                    if 59 < ballPos2[0] < 59 + w1 and y1 < ballPos2[1] < y1 + h1:
                        speedX2 = -speedX2
                        speedY2 = random_speed()
                        ballPos2[0] += 30
                        score[0] += 1
                        leftsound.play()

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos1[0] < 1195 and y1 < ballPos1[1] < y1 + h1:
                        speedX1 = -speedX1
                        speedY1 = random_speed()
                        ballPos1[0] -= 30
                        score[1] += 1
                        rightsound.play()

                    if 1195 - 50 < ballPos2[0] < 1195 and y1 < ballPos2[1] < y1 + h1:
                        speedX2 = -speedX2
                        speedY2 = random_speed()
                        ballPos2[0] -= 30
                        score[1] += 1
                        rightsound.play()

        if (ballPos1[0] < 40 or ballPos1[0] > 1200) and (ballPos2[0] < 40 or ballPos2[0] > 1200):
            gameOver1 = True
            gameOver2 = True

        if gameOver1 and gameOver2:
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)

            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played
                randomEndPhotoIndex = random.randrange(len(imgEndPhoto))
            img = imgEndPhoto[randomEndPhotoIndex]

        else:
            if ballPos1[1] >= 500 or ballPos1[1] <= 10:
                speedY1 = -speedY1
            if ballPos2[1] >= 500 or ballPos2[1] <= 10:
                speedY2 = -speedY2

            ballPos1[0] += speedX1
            ballPos1[1] += speedY1
            ballPos2[0] += speedX2
            ballPos2[1] += speedY2

            if check_ball_collision(ballPos1, ballPos2):
                speedX1, speedX2 = -speedX1, -speedX2
                speedY1, speedY2 = -speedY1, -speedY2

            img = cvzone.overlayPNG(img, imgBall, ballPos1)
            img = cvzone.overlayPNG(img, imgBall, ballPos2)

    if one_player:
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] += 30
                        score[0] += 1
                        leftsound.play()

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] -= 30
                        score[1] += 1
                        rightsound.play()
                        

        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True
            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played
                randomEndPhotoIndex = random.randrange(len(imgEndPhoto))

        if gameOver:
            img = imgEndPhoto[randomEndPhotoIndex]
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
        else:
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            img = cvzone.overlayPNG(img, imgBall, ballPos)

    if two_player:
        if hands:
                for hand in hands:
                    x, y, w, h = hand['bbox']
                    h1, w1, _ = imgBat1.shape
                    y1 = y - h1 // 2
                    y1 = np.clip(y1, 20, 415)

                    if hand['type'] == "Right":
                        img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                        if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] += 30
                            score[0] += 1
                            leftsound.play()

                    if hand['type'] == "Left":
                        img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                        if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] -= 30
                            score[1] += 1
                            rightsound.play()
                        

        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True
            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played
                randomEndPhotoIndex = random.randrange(len(imgEndPhoto))

        if gameOver:
            img = imgEndPhoto[randomEndPhotoIndex]
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
        else:
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            img = cvzone.overlayPNG(img, imgBall, ballPos)

    cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 5)
    cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 5)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if gameOver or (gameOver1 and gameOver2):
        img = imgGameOver
        showR_Width = cv2.getTextSize("Press R return to Login Page", cv2.FONT_HERSHEY_COMPLEX,2,2)[0][0]
        showESC_Width = cv2.getTextSize("Press ESC to Exit", cv2.FONT_HERSHEY_COMPLEX,2,2)[0][0]


        cv2.putText(img, "Press R return to Login Page",(-round(showR_Width/2) + round(img.shape[1]/2), 200), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
        cv2.putText(img, "Press ESC to Exit",(-round(showESC_Width/2) + round(img.shape[1]/2), 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 5)
        cv2.imshow("Image", img)
        key = cv2.waitKey(0)
    if key == 27:
        break
    if key == ord('r'):
        one_player = False
        two_player = False
        challenge_mode = False

        show_login_page()

        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        ballPos1 = [100, 100]  # Reset positions for challenge mode
        speedX1 = 15
        speedY1 = 15
        ballPos2 = [800, 450]
        speedX2 = 15
        speedY2 = 15
        gameOver = False
        gameOver1 = False
        gameOver2 = False
        gameOverSoundPlayed = False  # Reset the game over sound flag
        score = [0, 0]
        imgGameOver = cv2.resize(cv2.imread("Resources/newGameOver.png"),(1280,720))

        gameOverSound.stop()
        pygame.mixer.music.play()
        pygame.time.delay(2000)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
