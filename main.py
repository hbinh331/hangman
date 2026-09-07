import pygame
import math
from logic import HangmanGame

pygame.init()
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super vip pro hangman game")

FPS = 60
clock = pygame.time.Clock()

game = HangmanGame(word_list=None, max_tries=6)

# Fonts
font = pygame.font.SysFont("comicsans", 45)
WORD = pygame.font.SysFont("comicsans", 40)
TITLE = pygame.font.SysFont("comicsans", 70)

# Buttons setup
radius = 24
space = 20
letters = []
x_start = round((WIDTH - (radius * 2 + space) * 13) / 2)
y_start = 540

def reset_buttons():
    global letters
    letters = []
    for i in range(26):
        x = x_start + space * 2 + ((radius * 2 + space) * (i % 13))
        y = y_start + ((i // 13) * (space + radius * 2))
        letters.append([x, y, chr(65 + i), True])

reset_buttons()

def draw():
    win.fill((255, 255, 255))

    # Remaining guesses
    remaining_text = font.render(f"Guesses left: {game.tries_left}", 1, (0, 255, 0))
    win.blit(remaining_text, (10, 20))
    
    # Wrong guesses list
    start_x, start_y, max_width = 10, 250, 450
    current_line, line_y = "Wrong guesses: ", start_y

    for ltr in game.incorrect_guessed:
        test_line = current_line + ltr + " "
        if font.render(test_line, 1, (255, 0, 0)).get_width() > max_width:
            win.blit(font.render(current_line, 1, (255, 0, 0)), (start_x, line_y))
            line_y += font.get_height() + 5
            current_line = ltr + " "
        else:
            current_line = test_line

    if current_line:
        win.blit(font.render(current_line, 1, (255, 0, 0)), (start_x, line_y))

    # Title
    title = TITLE.render("Hangman", 1, (0, 0, 0))
    win.blit(title, (500, 10))

    # Display correctly guessed letters and space ('_')
    text = WORD.render(game.get_display_word(), 1, (0, 0, 0))
    win.blit(text, (WIDTH * 0.65 - text.get_width() / 2, 250))

    # Display letter buttons
    for x, y, ltr, visible in letters:
        if visible:
            pygame.draw.circle(win, (0, 0, 0), (x, y), radius, 4)
            txt = font.render(ltr, 1, (0, 0, 0))
            win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

    pygame.display.update()

def show_end_screen(won):
    win.fill((255, 255, 255))
    
    # Win - Lose notification
    status_str = "YOU WON!" if won else "YOU LOST!"
    color = (0, 200, 0) if won else (255, 0, 0)
    status_text = TITLE.render(status_str, 1, color)
    win.blit(status_text, (WIDTH / 2 - status_text.get_width() / 2, 150))

    # Display secret word
    answer_text = font.render(f"The secret word was: {game.secret_word}", 1, (0, 0, 0))
    win.blit(answer_text, (WIDTH / 2 - answer_text.get_width() / 2, 260))

    # Play again/Quit buttons
    btn_play = pygame.Rect(WIDTH / 2 - 180, 380, 180, 50)
    btn_quit = pygame.Rect(WIDTH / 2 + 20, 380, 180, 50)

    pygame.draw.rect(win, (0, 200, 0), btn_play, border_radius=10)
    pygame.draw.rect(win, (200, 0, 0), btn_quit, border_radius=10)

    btn_font = pygame.font.SysFont("comicsans", 26)
    play_txt = btn_font.render("PLAY AGAIN", 1, (255, 255, 255))
    quit_txt = btn_font.render("QUIT", 1, (255, 255, 255))

    win.blit(play_txt, (btn_play.x + (btn_play.width - play_txt.get_width()) / 2, 
                        btn_play.y + (btn_play.height - play_txt.get_height()) / 2))
    win.blit(quit_txt, (btn_quit.x + (btn_quit.width - quit_txt.get_width()) / 2, 
                        btn_quit.y + (btn_quit.height - quit_txt.get_height()) / 2))

    pygame.display.update()

    # Wait for user input
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Thoát game
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if btn_play.collidepoint(mx, my):
                    game.reset()       # Reset Logic
                    reset_buttons()    # Reset UI Buttons
                    return True        # PLay again
                
                if btn_quit.collidepoint(mx, my):
                    return False       # Quit game

# Game loop
run = True
while run:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = math.sqrt((x - x_mouse) ** 2 + (y - y_mouse) ** 2)
                    if dist <= radius:
                        letter[3] = False  # Make button invisible
                        game.guess(ltr)    # Process guess

    # Check game status
    if game.is_won() or game.is_lost():
        pygame.time.delay(500)
        run = show_end_screen(game.is_won())

pygame.quit()