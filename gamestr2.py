import tkinter as tk
import random
import cv2
from cvzone.HandTrackingModule import HandDetector
from PIL import Image, ImageTk


video = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)


def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!", 0
    elif (
        (player_choice == "Rock" and computer_choice == "Scissors")
        or (player_choice == "Paper" and computer_choice == "Rock")
        or (player_choice == "Scissors" and computer_choice == "Paper")
    ):
        return "You win!", 1
    else:
        return "Computer wins!", -1


def player_choice(choice):
    computer_choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(computer_choices)
    
    result, score_change = determine_winner(choice, computer_choice)
    
    global player_score, computer_score
    player_score += score_change
    computer_score -= score_change
    
    result_label.config(text=f"Computer chose {computer_choice}. {result}")
    score_label.config(text=f"Player: {player_score}  Computer: {computer_score}")


def capture_hand_gesture():
    success, img = video.read()
    
    if not success:
        return None
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    hands, img = detector.findHands(img)
    
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        
        if fingers == [0, 0, 0, 0, 0]:
            player_choice("Rock")
        elif fingers == [1, 1, 1, 1, 1]:
            player_choice("Paper")
        elif fingers == [0, 1, 1, 0, 0]:
            player_choice("Scissors")
    
    return img


def start_next_round():
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    result_label.config(text="")
    score_label.config(text=f"Player: {player_score}  Computer: {computer_score}")


root = tk.Tk()
root.title("Rock-Paper-Scissors Game")


player_score = 0
computer_score = 0

img_label = tk.Label(root)
img_label.pack()


result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

score_label = tk.Label(root, text=f"Player: {player_score}  Computer: {computer_score}", font=("Helvetica", 12))
score_label.pack()


next_round_button = tk.Button(root, text="Next Round", command=start_next_round)
next_round_button.pack()


def update_gui():
    img = capture_hand_gesture()
    
    if img is not None:
        pil_image = Image.fromarray(img)
        img_label.imgtk = ImageTk.PhotoImage(image=pil_image)
        img_label.config(image=img_label.imgtk)
    
    
    img_label.after(100, update_gui)  


root.after(100, update_gui)  
root.mainloop()
