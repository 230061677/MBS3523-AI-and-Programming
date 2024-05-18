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
leftBatY = 200
imshow = False
ballVel = [15, 15]

# Importing all images
imgtennisCourt = cv2.imread("Resources/peakpx.jpg")
imgGameOver = cv2.imread("Resources/newGameOver.png")
imgGameOver = cv2.resize(imgGameOver, (1280, 720))  # Resize game over image
imgEndPhoto = []
imgEndPhotoFolderName = 'gameEndPhoto'
for filename in os.listdir(imgEndPhotoFolderName):
    f = os.path.join(imgEndPhotoFolderName, filename)
    if os.path.isfile(f):
        imgEndPhoto.append(cv2.imread(f))

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

original_imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (85, 85))

def first_bat():
    global speedX, speedY, ballPos, score, imgBall
    speedX += 1
    speedY += 1
    ballPos[0] += 50
    imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
    speedX = -speedX
    score[0] += 1
    leftsound.play()

def second_bat():
    global speedX, speedY, ballPos, score, imgBall
    # Increase speed after collision
    speedX += 1
    speedY += 1
    ballPos[0] -= 80
    imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
    speedX = -speedX
    score[1] += 1
    rightsound.play()

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
speedX1 = 15
speedY1 = 15
gameOver1 = False
ballPos2 = [800, 450]
speedX2 = 15
speedY2 = 15
gameOver2 = False

def random_speed():
    return random.randint(50, 100)

def check_ball_collision(ballPos1, ballPos2):
    dist = np.linalg.norm(np.array(ballPos1) - np.array(ballPos2))
    return dist < 50

def show_game_over_screen():
    global imgGameOver, score
    img = imgGameOver.copy()
    gameOverSoundPlayed = gameOverSound
    cv2.putText(img, str(score[0]), (150, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
    cv2.putText(img, str(score[1]), (1050, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
    cv2.imshow("Image", img)
    if not gameOverSoundPlayed:
        gameOverSound.play()
        gameOverSoundPlayed = True
        newimg = imgEndPhoto[random.randrange(len(imgEndPhoto))]
        cv2.imshow("end", newimg)
        cv2.waitKey(1500)
        cv2.destroyWindow("end")
        imshow = True

# Game loop
while True:
    if not (gameOver or (challenge_mode and gameOver1 and gameOver2)):
        _, img = cap.read()
        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, flipType=False)
        imgtennisCourt = cv2.resize(imgtennisCourt,(img.shape[1],img.shape[0]))
        img = cv2.addWeighted(img, 0.2, imgtennisCourt, 0.8, 0)

        if one_player or two_player:
            if hands:
                hand1 = hands[0]
                x1, y1, w1, h1 = hand1['bbox']
                h1 = 200
                x1 = 100

                img = cvzone.overlayPNG(img, imgBat1, (x1, y1))

                if hand1['lmList']:
                    lmList = hand1['lmList']
                    rightHandY = lmList[5][1]  # Y-coordinate of the middle finger MCP
                    if 0 <= rightHandY <= 480:
                        leftBatY = rightHandY

            if two_player and len(hands) == 2:
                hand2 = hands[1]
                x2, y2, w2, h2 = hand2['bbox']
                h2 = 200
                x2 = 1080

                img = cvzone.overlayPNG(img, imgBat2, (x2, y2))


            # Check ball collision with paddles
            if ballPos[1] + speedY >= 700 or ballPos[1] + speedY <= 0:
                speedY = -speedY

            if ballPos[0] + speedX >= 1220:
                if two_player:
                    if y2 <= ballPos[1] <= y2 + h2:
                        second_bat()
                    else:
                        gameOver = True
                else:
                    gameOver = True

            if ballPos[0] + speedX <= 0:
                if one_player:
                    gameOver = True
                elif y1 <= ballPos[1] <= y1 + h1:
                    first_bat()
                else:
                    gameOver = True

            ballPos[0] += speedX
            ballPos[1] += speedY

            img = cvzone.overlayPNG(img, imgBall, ballPos)

            # Score display
            cv2.putText(img, str(score[0]), (300, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)
            cv2.putText(img, str(score[1]), (900, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)

            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break

            if challenge_mode:
                if check_ball_collision(ballPos1, ballPos2):
                    ballVel = [random_speed(), random_speed()]
                    ballPos1 = [100, 100]
                    ballPos2 = [800, 450]

                if ballPos1[1] + speedY1 >= 700 or ballPos1[1] + speedY1 <= 0:
                    speedY1 = -speedY1

                if ballPos1[0] + speedX1 >= 1220 or ballPos1[0] + speedX1 <= 0:
                    gameOver1 = True

                ballPos1[0] += speedX1
                ballPos1[1] += speedY1

                img = cvzone.overlayPNG(img, imgBall, ballPos1)

                if ballPos2[1] + speedY2 >= 700 or ballPos2[1] + speedY2 <= 0:
                    speedY2 = -speedY2

                if ballPos2[0] + speedX2 >= 1220 or ballPos2[0] + speedX2 <= 0:
                    gameOver2 = True

                ballPos2[0] += speedX2
                ballPos2[1] += speedY2

                img = cvzone.overlayPNG(img, imgBall, ballPos2)

                cv2.imshow("Image", img)
                key = cv2.waitKey(1)
                if key == 27:  # ESC key
                    break

    else:
        show_game_over_screen()
        cv2.waitKey(1)

    #cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
