from Graphic import *
from config import *
import pygame, sys
from Button import Button
pygame.init()

pygame.display.set_caption("Wumpus World")
map_pos = 0
change_map_list = ['map/map1.txt','map/map2.txt','map/map3.txt','map/map4.txt','map/map5.txt', 'map/map6.txt']

def display_map(maptext,screen,CELL_SIZE):
  wumpus1 = pygame.image.load("images/wumpus.png")
  breeze1 = pygame.image.load("images/breeze.png")
  stench1 = pygame.image.load("images/stench.png")
  gold1 = pygame.image.load("images/gold.png")
  pit1 = pygame.image.load("images/pit.png")

  wumpus1 = pygame.transform.scale(wumpus1, (CELL_SIZE, CELL_SIZE))
  breeze1 = pygame.transform.scale(breeze1, (CELL_SIZE, CELL_SIZE))
  stench1 = pygame.transform.scale(stench1, (CELL_SIZE, CELL_SIZE))
  gold1 = pygame.transform.scale(gold1, (CELL_SIZE, CELL_SIZE))
  pit1 = pygame.transform.scale(pit1, (CELL_SIZE, CELL_SIZE))

  N, cave, agent_pos = read_map(maptext)
  for row in range(len(cave)):
    for col in range(len(cave)):
      pygame.draw.rect(screen, WHITE, (get_map_pos_y(N, CELL_SIZE, 1280) + col * CELL_SIZE,
                                       get_map_pos_x(N, CELL_SIZE, 720) + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
      pygame.draw.rect(screen, BLACK, (get_map_pos_y(N, CELL_SIZE, 1280) + col * CELL_SIZE,
                                       get_map_pos_x(N, CELL_SIZE, 720) + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
      if cave[row, col] != "-":
        if "B" in cave[row, col]:
          screen.blit(breeze1, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE))
        if "W" in cave[row, col]:
          screen.blit(wumpus1, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE))
        if "S" in cave[row, col]:
          screen.blit(stench1, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE))
        if "G" in cave[row, col]:
          screen.blit(gold1, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE))
        if "P" in cave[row, col]:
          screen.blit(pit1, (get_map_pos_y(N, CELL_SIZE,1280) + col * CELL_SIZE,
                               get_map_pos_x(N, CELL_SIZE,720) + row * CELL_SIZE))

def play():
  global map_pos
  main(change_map_list[map_pos])

def options():
  global map_pos
  while True:
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    screen.blit(BG, (0, 0))
    display_map(change_map_list[map_pos],screen,30)
    OPTIONS_PREVIOUS = Button(image=None, pos=(300, 360),
                         text_input="<", font=get_font(40), base_color="White", hovering_color="Black")
    OPTIONS_NEXT = Button(image=None, pos=(980, 360),
                         text_input=">", font=get_font(40), base_color="White", hovering_color="Black")
    OPTIONS_BACK = Button(image=None, pos=(640, 600),
                       text_input="CONFIRM", font=get_font(20), base_color="White", hovering_color="Black")
    OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK.update(screen)

    for button in [OPTIONS_PREVIOUS, OPTIONS_NEXT, OPTIONS_BACK]:
      button.changeColor(OPTIONS_MOUSE_POS)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
          main_menu()
        if OPTIONS_PREVIOUS.checkForInput(OPTIONS_MOUSE_POS):
          if map_pos == 0:
            map_pos = len(change_map_list)-1
          else:
            map_pos -=1
        if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
          if map_pos == len(change_map_list) - 1:
            map_pos = 0
          else:
            map_pos += 1

    pygame.display.update()


def main_menu():
  while True:
    screen.blit(BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    # MENU_TEXT = get_font(30).render("Wumpus", True, BLACK)
    # MENU_RECT = MENU_TEXT.get_rect(center=(400, 50))
    PLAY_BUTTON = Button(image=None, pos=(640, 250),
                         text_input="PLAY", font=get_font(50), base_color=WHITE, hovering_color="Black")
    OPTIONS_BUTTON = Button(image=None, pos=(640, 400),
                            text_input="OPTIONS", font=get_font(50), base_color=WHITE, hovering_color="Black")
    QUIT_BUTTON = Button(image=None, pos=(640, 550),
                         text_input="QUIT", font=get_font(50), base_color=WHITE, hovering_color="Black")

    # screen.blit(MENU_TEXT, MENU_RECT)


    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
      button.changeColor(MENU_MOUSE_POS)
      button.update(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
          play()
        if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
          options()
        if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
          pygame.quit()
          sys.exit()

    pygame.display.update()