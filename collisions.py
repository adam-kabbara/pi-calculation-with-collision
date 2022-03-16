# references 
# https://en.wikipedia.org/wiki/Euler_method
# https://en.wikipedia.org/wiki/Elastic_collision

import copy
import pygame

pygame.init()
width = 500
height = 500
ground_height = height - 30
wall_width = 30
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Calculating PI with collisions')

timestep = 1000
digit_num = 4

class Block:
    def __init__(self, width, mass, velocity, color, x, y=None):
        self.mass = mass
        self.width = width
        self.velocity = velocity
        self.color = color
        self.x = x

        if y is None:
            self.y = ground_height - width

    def move(self):
        self.x -= self.velocity

    def collide(self, block):
        part1 = (self.mass - block.mass) / (self.mass + block.mass) * self.velocity
        part2 = 2 * block.mass / (self.mass + block.mass) * block.velocity
        new_velocity = part1 + part2
        self.velocity = new_velocity


    def draw(self, win): # round the decimal to the nearest full number sincewe can move obj a fraction of a pixel
        pygame.draw.rect(win, self.color, tuple(map(round, (self.x, self.y, self.width, self.width)))) # square
        pygame.draw.rect(win, (255, 255, 255), tuple(map(round, (self.x, self.y, self.width, self.width))), 1) # border


def redraw_window(boxes, count, complete):
    win.fill((0, 0, 0))
    for elem in boxes:
        elem.draw(win)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f"{count}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.topright = (width - 10, 20)
    win.blit(text, textRect)

    if complete:
        text = font.render(f"PI calculation complete", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        win.blit(text, textRect)
    
    # wall and ground
    pygame.draw.rect(win, (200, 200, 200), (0, ground_height, width, height))
    pygame.draw.rect(win, (200, 200, 200), (0, 0, wall_width, height))

    pygame.display.update()


def mainLoop():
    run = True
    fps = 60
    count = 0
    complete = False
    clock = pygame.time.Clock()
    b1 = Block(100, 100**digit_num, 2/timestep, (70, 70, 70), width - 120)
    b2 = Block(50, 1, 0, (120, 120, 120), 200)

    while run:

        for _ in range(timestep):
            b1.move()
            b2.move()
            if b1.x <= b2.x + b2.width and b1.x + b1.width >= b2.x:
                b1_copy, b2_copy = copy.deepcopy(b1), copy.deepcopy(b2) # create copies so we can access prev velocity
                b2.collide(b1_copy)
                b1.collide(b2_copy)
                count += 1

            if b2.x <= wall_width:
                b2.velocity *= -1
                count += 1

            #check completion
            if b2.velocity < 0 and b1.velocity < b2.velocity:
                complete = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        redraw_window([b1, b2], count, complete)
        clock.tick(fps)


if __name__ == '__main__':
    mainLoop()
