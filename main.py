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
        wboard = np.zeros((len(board), len(board)), dtype=int)
        wboard += board
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
        fit_pop.append((eat * eat) / t)  # fitness function
    return population, fit_pop


def calculate_fit(fit_pop):  # covert result functions result to percentiles
    per_fit = []
    for i in range(len(fit_pop)):
        per_fit.append(fit_pop[i] / sum(fit_pop))
    return per_fit


def selection(population, per_fit):
    calculation_fit = [0]  # it is created for calculate random
    selected_pop_ind = []
    A = np.zeros((len(population), len(population)), dtype=int)
    for i in range(len(per_fit) - 1):
        calculation_fit.append(sum(per_fit[0:i + 1]))
    calculation_fit.append(1)  # sometimes this value can be 0,99999

    print(calculation_fit)

    for j in range(len(per_fit)):
        select = random.random()
        print(select)
        for i in range(len(per_fit)):
            if select > calculation_fit[i] and select < calculation_fit[i + 1]:
                selected_pop_ind.append(i)
        #A = np.vstack([A, population[selected_pop_ind[j]]])
        print(population[selected_pop_ind[j]])
    print(selected_pop_ind)
    #print(new_pop)

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
for i in range(0, 10):
    print(i, ". nesil")
    print(board)
    population, fit_pop = work(board, population, fn, x, y)
    print("normal", fit_pop)
    print("yüzdelik", calculate_fit(fit_pop))
    selection(population, calculate_fit(fit_pop))
