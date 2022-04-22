import pytimedinput
import os
import random

class Game:
    def __init__(self, width=24, height=16):
        self.GAME_WIDTH = width
        self.GAME_HEIGHT = height
        self.board = [[0 for width in range(self.GAME_WIDTH)] for height in range(self.GAME_HEIGHT)]
        self.food = []
        self.generate_food()
        snake_starting_pos = (random.randint(2, self.GAME_HEIGHT-2), random.randint(2, self.GAME_WIDTH-2))
        self.snake = [snake_starting_pos]
        self.prev_key_input = 'w' # snake starts upwards

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("- - - TERMINAL SNAKE - - -".center(self.GAME_WIDTH * 2))
        print("CONTROLS: W A S D".center(self.GAME_WIDTH * 2))
        print(('SCORE: ' + str(len(self.snake))).center(self.GAME_WIDTH * 2))
        for i_r, row in enumerate(self.board):
            for i_c, column in enumerate(row):
                    if i_r in (0, self.GAME_HEIGHT-1) or i_c in (0, self.GAME_WIDTH-1):
                        print('#', end=' ')
                    elif (i_r, i_c) in self.snake:
                        print('X', end=' ')
                    elif (i_r, i_c) in self.food:
                        print('o', end=' ')
                    else:
                        print(' ', end=' ')
            print()

    def get_input(self):
        key, timeout = pytimedinput.timedKey(prompt="", timeout=0.4, allowCharacters="wasd")
        if timeout:
            key = self.prev_key_input
        self.prev_key_input = key
        return key

    def move_snake(self, key):
        direction = {'a': (0, -1),
                    'd': (0, 1),
                    'w': (-1, 0),
                    's': (1, 0),
        }
        key = str.lower(key)
        new_head = (self.snake[0][0] + direction[key][0], self.snake[0][1] + direction[key][1])
        self.snake.insert(0, new_head)
        self.check_and_handle_food_collision()
        return False

    def check_and_handle_food_collision(self):
        # if snake eats food, don't remove snake tail, and generate new food
        if self.snake[0] in self.food:
            self.food.pop()
            self.generate_food()
        else:
            self.snake.pop()

    def generate_food(self):
        # todo: prevent food spawning on a position occoupied by snake
        new_food = (random.randint(1, self.GAME_HEIGHT-2), random.randint(1, self.GAME_HEIGHT-2))
        self.food.append(new_food)

    def is_game_over(self):
        if self.snake[0] in self.snake[1:]:
            print('Snake hit itself.')
            return True
        if self.snake[0] in (0, self.GAME_HEIGHT-1) or self.snake[0] in (0, self.GAME_HEIGHT-1):
            print('Snake hit a wall.')
            return True   
        return False

    def run(self):
        while True:
            self.draw()
            key = self.get_input()
            self.move_snake(key)
            if self.is_game_over():
                print('GAME OVER.')
                break


if __name__ == '__main__':
    Game().run()