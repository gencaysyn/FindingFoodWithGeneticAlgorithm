import random
import numpy as np


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def generate_food(n, fn, a, b):
    foods = []
    for i in range(fn):
        while True:
            flag = 0
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            for f in foods:
                if (x == f.x and y == f.y) or (x == a and y == b):
                    flag = 1
            if flag == 0:
                break
        foods.append(Food(x, y))
    return foods


def place_foods(board, foods):
    for food in foods:
        board[food.x][food.y] = 1
    return board


def work(board, population, fn, x, y):
    fit_pop = []

    for p in range(len(population)):
        wboard = board
        i = x
        j = y
        eat = 0
        t = 0  # distance
        print("Person...........")
        while eat != fn and t < len(population[0]):
            if population[p][t] == 1:
                j -= 1
            elif population[p][t] == 2:
                i -= 1
            elif population[p][t] == 3:
                j += 1
            elif population[p][t] == 4:
                i += 1
            if i < 0 or j < 0 or i >= len(wboard) or j >= len(wboard):
                print("hit to wall!")
                break
            if wboard[i][j] == 1:
                eat += 1
            wboard[i][j] = 8
            t += 1
        print(wboard)
        print(eat)
        fit_pop.append((eat * eat) / t)
    return population, fit_pop


n = 5  # size of board
fn = 10  # number of food
m = 10  # number of step
p = 4  # population
# start point indexes
x = 2
y = 2
board = np.zeros((n, n), dtype=int)
foods = generate_food(n, fn, x, y)
board = place_foods(board, foods)
population = np.random.random_integers(4, size=(p, m))
board[x][y] = 8

# print(population)
# print(board)
for i in range(0,10):
    print("giriş")
    print(board)
    population, fit_pop = work(board, population, fn, x, y)
    print(fit_pop)
