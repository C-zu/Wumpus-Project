import pygame
import pandas as pd
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE= 80
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 14)

wumpus = pygame.image.load("images/wumpus.png")
agent = pygame.image.load("images/agent.png")
breeze = pygame.image.load("images/breeze.png")
stench = pygame.image.load("images/stench.png")
gold = pygame.image.load("images/gold.png")
pit = pygame.image.load("images/pit.png")
door = pygame.image.load("images/door.png")

wumpus = pygame.transform.scale(wumpus, (CELL_SIZE, CELL_SIZE))
agent = pygame.transform.scale(agent, (CELL_SIZE, CELL_SIZE))
breeze = pygame.transform.scale(breeze, (CELL_SIZE, CELL_SIZE))
stench = pygame.transform.scale(stench, (CELL_SIZE, CELL_SIZE))
gold = pygame.transform.scale(gold, (CELL_SIZE, CELL_SIZE))
pit = pygame.transform.scale(pit, (CELL_SIZE, CELL_SIZE))
door = pygame.transform.scale(door, (CELL_SIZE, CELL_SIZE))

def get_map_pos_y(N,CELL_SIZE):
    return WIDTH // 2 - (CELL_SIZE * N // 2)
def get_map_pos_x(N,CELL_SIZE):
    return HEIGHT // 2 - (CELL_SIZE * N // 2)

def read_map(filepath):
    with open(filepath, 'r') as file:
        n = int(file.readline())
        df = pd.read_csv(filepath,sep=".", header=None, skiprows=1)
        return n,df

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus")
map = read_map("map/map1.txt")
def create_map(map):
    N = map[0]
    df = map[1]
    for row in range(N):
        for col in range(N):
            if (df.iloc[row,col] != "-"):
                if "B" in df.iloc[row,col]:
                    screen.blit(breeze, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                        get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "W" in df.iloc[row, col]:
                    screen.blit(wumpus, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "S" in df.iloc[row, col]:
                    screen.blit(stench, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "G" in df.iloc[row, col]:
                    screen.blit(gold, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "D" in df.iloc[row, col]:
                    screen.blit(door, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "A" in df.iloc[row, col]:
                    screen.blit(agent, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
                if "P" in df.iloc[row, col]:
                    screen.blit(pit, (get_map_pos_y(N, CELL_SIZE) + col * CELL_SIZE,
                                         get_map_pos_x(N, CELL_SIZE) + row * CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            text = FONT.render(f"({col + 1},{N - row})", True, BLACK)
            text_rect = text.get_rect()
            text_rect.bottomleft = (col * CELL_SIZE, (row + 1) * CELL_SIZE)
            screen.blit(text, text_rect)
def main():
    run = True
    while run:
        screen.fill(WHITE)
        create_map(map)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()