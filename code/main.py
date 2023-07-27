import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Slashy Souls")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():   # events are all events in the sense of
                if event.type == pygame.QUIT:  # inputs, or things that need to be computed
                    pygame.quit()              # they are held inside a buffer
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)




if __name__ == '__main__':
    game = Game()
    game.run()



