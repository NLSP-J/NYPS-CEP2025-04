''' ---------- IMPORT WORD FROM WORD LIST ---------- '''
import random, time
import pygame as pg
pg.init()
import asyncio

import words as w

random.seed(time.time())
L = w.word_list

# Set the full window width and height
win_width = 500
win_height = 700  # Reduced height since boxes are smaller
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Guess The Word')

# Fonts
font_large = pg.font.Font(None, 32)  # Smaller font for smaller boxes
font_medium = pg.font.Font(None, 40)
font_small = pg.font.Font(None, 25)  # Smaller font for keyboard

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)

# Game variables
word = L[random.randint(0,len(L))]
game_board = [[' ' for _ in range(5)] for _ in range(6)]
count = 0
letters = 0
game_over = False
running = True

# Keyboard tracking
keyboard = {
    'Q': gray, 'W': gray, 'E': gray, 'R': gray, 'T': gray, 'Y': gray, 'U': gray, 'I': gray, 'O': gray, 'P': gray,
    'A': gray, 'S': gray, 'D': gray, 'F': gray, 'G': gray, 'H': gray, 'J': gray, 'K': gray, 'L': gray,
    'Z': gray, 'X': gray, 'C': gray, 'V': gray, 'B': gray, 'N': gray, 'M': gray
}

''' ---------- DRAW FUNCTIONS ---------- '''
def draw_board():
    # Game board with smaller boxes (60px instead of 75px)
    box_size = 60
    padding = 5
    start_x = win_width//2 - (5 * (box_size + padding))//2
    start_y = 20
    
    for col in range(5):
        for row in range(6):
            square = pg.Rect(
                start_x + col * (box_size + padding),
                start_y + row * (box_size + padding),
                box_size, box_size
            )
            
            # Determine square color
            if count > row:
                if word[col] == game_board[row][col]:
                    color = green
                elif game_board[row][col] in word:
                    color = yellow
                else:
                    color = dark_gray
            else:
                color = white if row == count and not game_over else gray
            
            pg.draw.rect(screen, color, square, border_radius=3)
            
            letter_text = font_large.render(game_board[row][col].upper(), True, black if color == white else white)
            text_rect = letter_text.get_rect(center=square.center)
            screen.blit(letter_text, text_rect)

def draw_keyboard():
    # Position keyboard higher up (starting at 500 instead of 550)
    keyboard_start_y = 500
    key_width = 35
    key_height = 45
    key_padding = 5
    
    # First row (Q-P)
    for i, key in enumerate(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']):
        key_rect = pg.Rect(
            win_width//2 - (10 * (key_width + key_padding))//2 + i * (key_width + key_padding),
            keyboard_start_y,
            key_width, key_height
        )
        pg.draw.rect(screen, keyboard[key], key_rect, border_radius=3)
        key_text = font_small.render(key, True, white)
        text_rect = key_text.get_rect(center=key_rect.center)
        screen.blit(key_text, text_rect)
    
    # Second row (A-L)
    for i, key in enumerate(['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']):
        key_rect = pg.Rect(
            win_width//2 - (9 * (key_width + key_padding))//2 + i * (key_width + key_padding),
            keyboard_start_y + key_height + key_padding,
            key_width, key_height
        )
        pg.draw.rect(screen, keyboard[key], key_rect, border_radius=3)
        key_text = font_small.render(key, True, white)
        text_rect = key_text.get_rect(center=key_rect.center)
        screen.blit(key_text, text_rect)
    
    # Third row (Z-M)
    for i, key in enumerate(['Z', 'X', 'C', 'V', 'B', 'N', 'M']):
        key_rect = pg.Rect(
            win_width//2 - (7 * (key_width + key_padding))//2 + i * (key_width + key_padding),
            keyboard_start_y + 2 * (key_height + key_padding),
            key_width, key_height
        )
        pg.draw.rect(screen, keyboard[key], key_rect, border_radius=3)
        key_text = font_small.render(key, True, white)
        text_rect = key_text.get_rect(center=key_rect.center)
        screen.blit(key_text, text_rect)

def update_keyboard():
    for row in range(count):
        for col in range(5):
            letter = game_board[row][col].upper()
            if letter in keyboard:
                if word[col] == game_board[row][col]:
                    keyboard[letter] = green
                elif game_board[row][col] in word:
                    if keyboard[letter] != green:
                        keyboard[letter] = yellow
                else:
                    if keyboard[letter] not in [green, yellow]:
                        keyboard[letter] = dark_gray

def draw_win():
    if game_over:
        if any(''.join(row) == word for row in game_board):
            result_text = "Winner!"
            color = green
        else:
            result_text = f"Word: {word.upper()}"
            color = white
        
        text = font_medium.render(result_text, True, color)
        screen.blit(text, (win_width//2 - text.get_width()//2, 450))

''' ---------- GAME FUNCTIONS ---------- '''
def check_match():
    global game_over
    for row in range(6):
        guess = ''.join(game_board[row])
        if guess == word and row < count:
            game_over = True
    
    if count == 6:
        game_over = True

''' ---------- MAIN GAME LOOP ---------- '''
async def main():
    global running, game_over, game_board, letters, count, word

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
            if event.type == pg.TEXTINPUT and letters < 5 and not game_over:
                entry = event.text.upper()
                if entry.isalpha():
                    game_board[count][letters] = entry.lower()
                    letters += 1
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and letters > 0:
                    game_board[count][letters - 1] = ' '
                    letters -= 1
                    
                if event.key == pg.K_RETURN and not game_over and letters == 5:
                    count += 1
                    letters = 0
                    check_match()
                    update_keyboard()
                    
                if event.key == pg.K_r and game_over:
                    # Reset game
                    word = random.choice(w.word_list)
                    game_board = [[' ' for _ in range(5)] for _ in range(6)]
                    count = 0
                    letters = 0
                    game_over = False
                    for key in keyboard:
                        keyboard[key] = gray
        
        screen.fill(black)
        draw_board()
        draw_keyboard()
        draw_win()
        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())