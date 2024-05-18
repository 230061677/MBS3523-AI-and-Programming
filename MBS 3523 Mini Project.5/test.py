import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame
import os
import time
from PIL import ImageFont, ImageDraw, Image

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
imgEndPhoto = []
imgEndPhotoFolderName = 'fullScreenGameEndPhoto'
for filename in os.listdir(imgEndPhotoFolderName):
    f = os.path.join(imgEndPhotoFolderName, filename)
    if os.path.isfile(f):
        imgEndPhoto.append(cv2.imread(f))

imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (60, 60))
# imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (60, 60))
imgBat1 = cv2.resize(cv2.imread("Resources/leftPat.png", cv2.IMREAD_UNCHANGED), (50, 150))
imgBat2 = cv2.resize(cv2.imread("Resources/rightPat.png", cv2.IMREAD_UNCHANGED), (50, 150))
# imgBat1 = cv2.resize(cv2.imread("Resources/leftPat.png", cv2.IMREAD_UNCHANGED), (52, 141))
# imgBat2 = cv2.resize(cv2.imread("Resources/rightPat.png", cv2.IMREAD_UNCHANGED), (52, 141))
#original_imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (85, 85))
original_imgBall = cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (60, 60))

background_imgBall = cv2.flip(cv2.resize(cv2.imread("Resources/kirby.png", cv2.IMREAD_UNCHANGED), (150, 150)),1)

# backgound img
marioback = cv2.imread("Resources/peakpx.jpg")
Uninverse = cv2.imread("Resources/universe.png")
# two_back = cv2.imread("Resources/wp4710895-entrance-to-autumn-wallpapers.jpg")
imgGameOver = cv2.imread("Resources/gameOver.png")


# Load music effects
default_music = 'sound/Kirbys Dream Land  Green Greens.mp3'
pygame.mixer.music.load(default_music)
challenge_music = 'sound/Gusty Garden Galaxy Theme  Super Mario Galaxy.mp3'
# two_music = 'sound\Paper Mario  The Origami King  Autumn Mountain Battle Theme Normal  Lineup Looped.mp3'
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
vs_bot = False

def aifirst_bat(hand, hand_type: str):  # the bottom is not working
    global speedX, speedY, ballPos, score, imgBall, img
    if hand['type'] == hand_type:
        hand_x, hand_y, hand_w, hand_h = hand['bbox']
        Bat_h, Bat_w, _ = imgBat1.shape
        y1 = hand_y - Bat_h // 2
        y1 = np.clip(y1, 20, 415)
        img = cvzone.overlayPNG(img, imgBat1, (59, y1))
        if 59 < ballPos[0] < 59 + Bat_w and (
                y1 < ballPos[1] + imgBall.shape[0] // 2 or y1 + Bat_h < ballPos[1] - imgBall.shape[0] // 2):
            speedX -= 1
            ballPos[0] += 50
            imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
            speedX = -speedX
            score[0] += 1
            leftsound.play()


def aisecond_bat(hand, hand_type: str):  # the bottom is not working
    global speedX, speedY, ballPos, score, imgBall, img
    if hand['type'] == hand_type:
        hand_x, hand_y, hand_w, hand_h = hand['bbox']
        Bat_h, Bat_w, _ = imgBat1.shape
        y1 = hand_y - Bat_h // 2
        y1 = np.clip(y1, 20, 415)
        img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
        if 1195 - 50 < ballPos[0] < 1195 and (
                y1 < ballPos[1] + imgBall.shape[0] // 2 or y1 + Bat_h < ballPos[1] - imgBall.shape[0] // 2):
            speedX += 1
            ballPos[0] -= 80
            imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
            speedX = -speedX
            score[1] += 1
            rightsound.play()

def countdown():
    for i in range(3, 0, -1):
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgtennisCourt = marioback
        imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
        blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
        img = blended_img

        hands, img = detector.findHands(img, flipType=False)
        ballPos1 = [100, 100]  # Reset positions for challenge mode
        ballPos2 = [800, 450]
        cvzone.overlayPNG(img, imgBall, (ballPos1[0], ballPos1[1]))
        cvzone.overlayPNG(img, imgBall, (ballPos2[0], ballPos2[1]))

        # for hand in hands:
        #     x, y, w, h = hand['bbox']
        #     if hand['type'] == "Left":
        #         img = cvzone.overlayPNG(img, imgBat1, (x, y))
        #     if hand['type'] == "Right":
        #         img = cvzone.overlayPNG(img, imgBat2, (x, y))
        
        cv2.putText(img, str(i), (600, 400), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 10)
        cv2.imshow("Image", img)
        cv2.waitKey(500)

    # Final "START" message
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
    blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
    img = blended_img

    hands, img = detector.findHands(img, flipType=False)

    for hand in hands:
        x, y, w, h = hand['bbox']
        if hand['type'] == "Left":
            img = cvzone.overlayPNG(img, imgBat1, (x, y))
        if hand['type'] == "Right":
            img = cvzone.overlayPNG(img, imgBat2, (x, y))

    cv2.putText(img, "START", (500, 400), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 10)
    ballPos1 = [100, 100]  # Reset positions for challenge mode
    ballPos2 = [800, 450]
    cvzone.overlayPNG(img, imgBall, (ballPos1[0], ballPos1[1]))
    cvzone.overlayPNG(img, imgBall, (ballPos2[0], ballPos2[1]))
    cv2.imshow("Image", img)
    cv2.waitKey(500)

def overlay_image(background, overlay, x, y):
    bg_height, bg_width = background.shape[:2]
    ol_height, ol_width = overlay.shape[:2]

    if x >= bg_width or y >= bg_height:
        return
    if x + ol_width > bg_width:
        ol_width = bg_width - x
        overlay = overlay[:, :ol_width]
    if y + ol_height > bg_height:
        ol_height = bg_height - y
        overlay = overlay[:ol_height]

    alpha_s = overlay[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        background[y:y + ol_height, x:x + ol_width, c] = (alpha_s * overlay[:, :, c] +
                                                          alpha_l * background[y:y + ol_height, x:x + ol_width, c])


def first_bat():
    global speedX, speedY, ballPos, score, imgBall
    speedX = speedX - 1
    speedX = -speedX
    
    
    ballPos[0] += 50
    imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
    
    score[0] += 1
    leftsound.play()
    

def second_bat():
    global speedX, speedY, ballPos, score, imgBall
    # Increase speed after collision
    speedX = abs(speedX) + 1
    speedX = -speedX
    
    

    ballPos[0] -= 80
    imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
    score[1] += 1
    rightsound.play()


def show_login_page():
    global one_player, two_player, challenge_mode, vs_bot, img, imgtennisCourt
    # Load the custom font
    font_path = "Resources/Pretendo.ttf"  # Path to your custom font file
    font = ImageFont.truetype(font_path, 80)  # Adjust size as needed

    while not (one_player or two_player or challenge_mode or vs_bot):
        _, img = cap.read()
        img = cv2.flip(img, 1)
        imgtennisCourt_resized = cv2.resize(marioback, (img.shape[1], img.shape[0]))
        blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
        img = blended_img

        hands, img = detector.findHands(img, flipType=False)

        button1_pos = (490, 270, 790, 320)  
        button2_pos = (490, 370, 790, 420)  
        button3_pos = (490, 470, 790, 520)  
        button4_pos = (490, 570, 790, 620)  

        # Add a title with custom font
        title_text = "Kirby's BOUNCE Journey"
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        # draw.text((100, 50), title_text, font=font, fill=(255, 255, 255, 255))
        draw.text((100, 100), title_text, font=font, fill=(0, 0, 0, 255))
        img = np.array(img_pil)
        
        # Position for the image near the title
        imgBall_x = 1000  # Adjust x position as needed
        imgBall_y = 170  # Adjust y position as needed
        # Overlay the image near the title
        overlay_image(img, background_imgBall, imgBall_x, imgBall_y)

        cv2.rectangle(img, (button1_pos[0], button1_pos[1]), (button1_pos[2], button1_pos[3]), (0, 0, 255), -1)
        cv2.rectangle(img, (button2_pos[0], button2_pos[1]), (button2_pos[2], button2_pos[3]), (0, 0, 255), -1)
        cv2.rectangle(img, (button3_pos[0], button3_pos[1]), (button3_pos[2], button3_pos[3]), (0, 0, 255), -1)
        cv2.rectangle(img, (button4_pos[0], button4_pos[1]), (button4_pos[2], button4_pos[3]), (0, 0, 255), -1)

        cv2.putText(img, "1 Player", (button1_pos[0] + 30, button1_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, "2 Players", (button2_pos[0] + 30, button2_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, "Challenge Mode", (button3_pos[0] + 10, button3_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)
        cv2.putText(img, "VS Bot", (button4_pos[0] + 50, button4_pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:  
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()

        def mouse_click(event, x, y, flags, param):
            global one_player, two_player, challenge_mode, vs_bot
            if event == cv2.EVENT_LBUTTONDOWN:
                if button1_pos[0] <= x <= button1_pos[2] and button1_pos[1] <= y <= button1_pos[3]:
                    one_player = True
                    pygame.mixer.music.load('sound/Kirbys Dream Land  Green Greens.mp3')
                    # Play challenge mode music
                    pygame.mixer.music.play(-1, 0.0, 0)
                elif button2_pos[0] <= x <= button2_pos[2] and button2_pos[1] <= y <= button2_pos[3]:
                    two_player = True
                    pygame.mixer.music.load('sound/Kirbys Dream Land  Green Greens.mp3')
                    # Play challenge mode music
                    pygame.mixer.music.play(-1, 0.0, 0)
                elif button3_pos[0] <= x <= button3_pos[2] and button3_pos[1] <= y <= button3_pos[3]:
                    # pygame.mixer.music.load('sound\Paper Mario  The Origami King  Autumn Mountain Battle Theme Normal  Lineup Looped.mp3')
                    # # Play challenge mode music
                    # pygame.mixer.music.play(-1, 0.0, 0)
                    pygame.mixer.music.load('sound/Kirbys Dream Land  Green Greens.mp3')
                    # Play challenge mode music
                    pygame.mixer.music.play(-1, 0.0, 0)
                    countdown()
                    challenge_mode = True
                elif button4_pos[0] <= x <= button4_pos[2] and button4_pos[1] <= y <= button4_pos[3]:
                    vs_bot = True
                    pygame.mixer.music.load('sound/Gusty Garden Galaxy Theme  Super Mario Galaxy.mp3')
                    # Play challenge mode music
                    pygame.mixer.music.play(-1, 0.0, 0)
                    

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

def check_ball_collision(ballPos1, ballPos2):
    dist = np.linalg.norm(np.array(ballPos1) - np.array(ballPos2))
    return dist < 50


left_hand_buf = {'type': 'Left', 'bbox': [0, 0, 0, 0]}
right_hand_buf = {'type': 'Right', 'bbox': [0, 0, 0, 0]}


def fix_hands(hands):
    output_hands = hands
    if len(hands) == 1 and not vs_bot:
        output_hands.append(left_hand_buf if hands[0]['type'] == 'Right' else right_hand_buf)
    elif len(hands) == 0:
        if not vs_bot: output_hands.append(left_hand_buf)
        output_hands.append(right_hand_buf)
    return output_hands


def find_in_(handtype: str, hands):
    res = None
    for i in range(len(hands)):
        if hands[i]['type'] == handtype:
            res = i
            break
    return res


def update_hand_bufs(hands):
    global left_hand_buf, right_hand_buf
    li, ri = find_in_("Left", hands), find_in_("Right", hands)
    if li is not None: left_hand_buf = hands[li]
    if ri is not None: right_hand_buf = hands[ri]

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    hands, img = detector.findHands(img, flipType=False)  # with draw
    update_hand_bufs(hands)
    hands = fix_hands(hands)
    
    if vs_bot:
        # Load background image for vs_bot mode
        imgtennisCourt = Uninverse
    # elif challenge_mode:
    #     imgtennisCourt = two_back
    else:
        imgtennisCourt = marioback

    imgtennisCourt_resized = cv2.resize(imgtennisCourt, (img.shape[1], img.shape[0]))
    blended_img = cv2.addWeighted(img, 0.2, imgtennisCourt_resized, 0.8, 0)
    img = blended_img
    

    if one_player:
        print(speedX)
        # print(speedY)
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        first_bat()
                        
                        
                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        second_bat()
                        

                        

        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True
            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played
                newimg = imgEndPhoto[random.randrange(len(imgEndPhoto))]
                cv2.imshow("end", newimg)
                cv2.waitKey(1500)
                cv2.destroyWindow("end")
                imshow = True
            

        if gameOver:
            img = imgGameOver
            # Reset imgBall to its original orientation
            imgBall = original_imgBall
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
            
        else:
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY
            ballPos[0] += speedX
            ballPos[1] += speedY

            img = cvzone.overlayPNG(img, imgBall, ballPos)


    if challenge_mode:
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos1[0] < 59 + w1 and y1 < ballPos1[1] < y1 + h1:
                        # Increase speed after collision
                        speedX1 = speedX1 - 1
                        ballPos1[0] += 50
                        imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
                        speedX1 = -speedX1
                        score[0] += 1
                        leftsound.play()

                    if 59 < ballPos2[0] < 59 + w1 and y1 < ballPos2[1] < y1 + h1:
                        # Increase speed after collision
                        # speedX2 = abs(speedX2) + 1
                        speedX2 = speedX2 - 1
                        ballPos2[0] += 30
                        imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
                        speedX2 = -speedX2
                        score[0] += 1
                        rightsound.play()

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos1[0] < 1195 and y1 < ballPos1[1] < y1 + h1:
                        # Increase speed after collision
                        speedX1 = abs(speedX1) + 1
                        ballPos1[0] -= 50
                        imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
                        speedX1 = -speedX1
                        score[1] += 1
                        leftsound.play()

                    if 1195 - 50 < ballPos2[0] < 1195 and y1 < ballPos2[1] < y1 + h1:
                        # Increase speed after collision
                        # speedX2 = speedX2 - 1
                        speedX2 = abs(speedX2) + 1
                        ballPos2[0] -= 30
                        imgBall = cv2.flip(imgBall, 1)  # Flip the ball image along the Y-axis
                        speedX2 = -speedX2
                        score[1] += 1
                        rightsound.play()

        if (ballPos1[0] < 40 or ballPos1[0] > 1200) and (ballPos2[0] < 40 or ballPos2[0] > 1200):
            gameOver1 = True
            gameOver2 = True

        if gameOver1 and gameOver2:
            img = imgGameOver
            # Reset imgBall to its original orientation
            imgBall = original_imgBall
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played
                newimg = imgEndPhoto[random.randrange(len(imgEndPhoto))]
                cv2.imshow("end", newimg)
                cv2.waitKey(1500)
                cv2.destroyWindow("end")
                imshow = True
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
                            first_bat()

                    if hand['type'] == "Left":
                        img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                        if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                            second_bat()
                        

        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True
            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played
                newimg = imgEndPhoto[random.randrange(len(imgEndPhoto))]
                cv2.imshow("end", newimg)
                cv2.waitKey(1500)
                cv2.destroyWindow("end")
                imshow = True

        if gameOver:
            img = imgGameOver
            # Reset imgBall to its original orientation
            imgBall = original_imgBall
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
        else:
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            img = cvzone.overlayPNG(img, imgBall, ballPos)

    if vs_bot:
        h1 = 197
        w1 = 73
        # Automatic movement for the left bat (AI)
        h1, w1, _ = imgBat1.shape
        # targetY = int(ballPos[1] + (ballPos[0] - 59) * (ballVel[1] / ballVel[0]))
        targetY = int(ballPos[1])
        # cv2.line(img, (0, targetY), (img.shape[1], targetY), (255, 0, 0), 1)
        leftBatY += int((targetY - leftBatY) * 0.2)  # Simple proportional control
        leftBatY = np.clip(leftBatY, 20, 415)
        # img = cvzone.overlayPNG(img, imgBat1, (59, leftBatY))
        # if 59 < ballPos[0] < 59 + w1 and leftBatY < ballPos[1] < leftBatY + h1:
        #     ballVel[0] = -ballVel[0]
        #     ballPos[0] += 30
        #     score[0] += 1
        ai_hand = {"type": "ai", "bbox": [None, leftBatY, None, None]}
        aifirst_bat(ai_hand, "ai")
        if hands:
            for hand in hands:
                # if hand['type'] == "Left":
                #     img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                #     if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                #         first_bat()

                aisecond_bat(hand, "Right")

        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True
            if not gameOverSoundPlayed:  # Check if the game over sound has already been played
                gameOverSound.play()  # Play the game over sound
                gameOverSoundPlayed = True  # Set the flag to True to indicate the sound has been played

        if gameOver:
            img = imgGameOver
            # Reset imgBall to its original orientation
            imgBall = original_imgBall
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5,
                        (200, 0, 200), 5)
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
    if key == 27:
        break
    if key == ord('r'):
        one_player = False
        two_player = False
        challenge_mode = False
        vs_bot = False
        imshow = False
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
        imgGameOver = cv2.imread("Resources/gameOver.png")
        gameOverSound.stop()
        pygame.mixer.music.play()
        pygame.time.delay(2000)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
