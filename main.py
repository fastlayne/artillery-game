import pygame
import sys
import logging
from typing import Optional
from game_manager import GameManager
from constants import WIDTH, HEIGHT, FPS, COLORS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Game:
    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.game_manager: Optional[GameManager] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.running: bool = False
        
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Artillery Game")
            self.clock = pygame.time.Clock()
            self.running = True
            self.game_manager = GameManager(self.screen)
            logger.info("Game initialized")
        except Exception as e:
            logger.critical(f"Failed to initialize game: {e}")
            self.quit(error=True)

    def run(self) -> None:
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    self.game_manager.handle_input(event)

                self.game_manager.update()
                self.game_manager.draw()
                pygame.display.flip()
                self.clock.tick(FPS)

            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                self.running = False

        self.quit()

    def quit(self, error: bool = False) -> None:
        logger.info("Shutting down game")
        try:
            pygame.quit()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        finally:
            sys.exit(1 if error else 0)

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)
