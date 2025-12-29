#!/usr/bin/python3


import pygame

from engine import engine

WIDTH = 640
HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS # better define width and height base on the squares?
IMAGES = {}
TOOLS = ["rs", "dr"] # dr - drawing

def load_images(): # better to implement in resources.py
    # first letter corresponds to the colour and the second - the name of the piece: wp - white pawn
    pieces = ['wp', 'wr', 'wn', 'wk', 'wq', 'wb', 'bp', 'br', 'bn', 'bk', 'bq', 'bb']  # maybe make it global
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load("./images/" + p + '.png'), (SQ_SIZE, SQ_SIZE))

    for t in TOOLS:
        IMAGES[t] = pygame.transform.scale(pygame.image.load("./images/" + t + '.png'), (SQ_SIZE, SQ_SIZE))

    highlights = ["cl"] # change later
    for h in highlights:
        IMAGES[h] = pygame.transform.scale(pygame.image.load("./images/" + h + ".png"), (SQ_SIZE, SQ_SIZE))


def main(): # limit the frames 
    pygame.init()
    running = True
    name = 'Board'
    game = engine()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(name)
    load_images()

    clicks = []
    sq_clicked = () # square which was clicked (x, y)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # the location (x, y) of the mouse on the board when clicked
                col = int(location[0] // SQ_SIZE)
                row = int(location[1] // SQ_SIZE)
                game.highlights = []
                if col > 7: # meaning the tools are being used (fix the hardcoding later)
                    if col == 8 and row == 0:
                        sq_clicked = ()
                        clicks = []
                        restart(game) # better to implement in engine.py
                    elif col == 9 and row == 0:
                        pass # implement drawing here
                elif sq_clicked == (col, row):  # check if the last click was on the same square, if so clear the sq_clicked 
                    sq_clicked = ()
                    clicks = []
                else:
                    sq_clicked = (col, row)
                    clicks.append(sq_clicked)
                    hl_pos_moves(sq_clicked, game)
                if len(clicks) == 2: # if two squares were clicked and they're not the same then make a move
                    print(clicks)
                    if not game.board[clicks[0][1]][clicks[0][0]]:
                        clicks = []
                        game.highlights.append(sq_clicked)
                    else:
                        game.make_move(clicks)
                        sq_clicked = ()
                        clicks = []
                        game.highlights = []
        draw_board(screen)
        draw_objects(screen, game.board, game.highlights)
        pygame.display.flip()
        

def draw_board(screen):
    colours = [pygame.Color('white'), pygame.Color('grey')]
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            colour = colours[(column + row) % 2]
            pygame.draw.rect(screen, colour, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))



def draw_objects(screen, board, highlights):
    # print(highlights)
    # draw pieces
    for row in range(DIMENSIONS):          # col - x, row - y
        for col in range(DIMENSIONS):
            if board[row][col]: # if a square is not empty draw the image for that particular square
                screen.blit(IMAGES[board[row][col]], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # draw highlights
    for h in highlights:
        screen.blit(IMAGES["cl"], pygame.Rect(h[0] * SQ_SIZE, h[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # draw tools
    tool_num = 2 # maybe make it global
    for i, t in enumerate(TOOLS):
        pygame.draw.rect(screen, "green", pygame.Rect(((i % 2) + DIMENSIONS) * SQ_SIZE, (i // tool_num) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(IMAGES[t], pygame.Rect(((i % 2) + DIMENSIONS) * SQ_SIZE, (i // tool_num) * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def restart(game):
    game.log = []
    game.highlights = []
    game.reset()
        

def hl_pos_moves(square, game):
    game.highlights.append(square) # add the pressed square itself
    # add other squares where the piece can move to


if __name__ == '__main__':
    main()