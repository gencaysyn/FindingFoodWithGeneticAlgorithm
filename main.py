import random
import numpy as np
import matplotlib.pyplot as plt


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
            if x == a and y == b:
                flag = 1
            for f in foods:
                if x == f.x and y == f.y:
                    flag = 1
            if flag == 0:
                break
        foods.append(Food(x, y))
    return foods


def place_foods(board, foods):
    for food in foods:
        board[food.x][food.y] = 1  # Food color
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
        plt.cla()
        plt.imshow(wboard)
        plt.pause(0.0000001)
        while eat != fn and t < len(population[0]):
            old_i = i
            old_j = j
            if population[p][t] == 1:
                j -= 1
            elif population[p][t] == 2:
                i -= 1
            elif population[p][t] == 3:
                j += 1
            elif population[p][t] == 4:
                i += 1
            if i < 0 or j < 0 or i >= len(wboard) or j >= len(wboard):
                # print("hit to wall!")
                break
            if wboard[i][j] == 1:  # Food color
                eat += 1
            wboard[old_i][old_j] = 8
            wboard[i][j] = 15
            t += 1
            plt.cla()
            plt.imshow(wboard)
            plt.pause(0.00000001)
            if eat == fn:
                break
        fit_pop.append(eat / fn)
        if eat == fn:
            break
        # plt.matshow(wboard)
        # plt.show()
        # print(wboard)
        # print(eat)
        # fit_pop.append((eat * eat) / t)  # fitness function
    return population, fit_pop


def show_board(board):
    plt.imshow(board)
    plt.pause(0.001)


def calculate_fit(fit_pop):  # covert result functions result to percentiles
    per_fit = []
    for i in range(len(fit_pop)):
        if sum(fit_pop) != 0:
            per_fit.append(fit_pop[i] / sum(fit_pop))
        else:
            per_fit.append(0)
    return per_fit


def selection(population, per_fit):
    calculation_fit = [0]  # it is created for calculate random
    selected_pop_ind = []
    new_pop = np.zeros((len(population), len(population[0])), dtype=int)
    for i in range(len(per_fit) - 1):
        calculation_fit.append(sum(per_fit[0:i + 1]))
    calculation_fit.append(1)  # sometimes this value can be 0,99999

    # print(calculation_fit)

    for j in range(len(per_fit)):
        select = random.random()
        for i in range(len(per_fit)):
            if select > calculation_fit[i] and select < calculation_fit[i + 1]:
                selected_pop_ind.append(i)
        new_pop = np.delete(new_pop, 0, 0)
        new_pop = np.append(new_pop, np.array([population[selected_pop_ind[j]]]), axis=0)
    # print("Selected Generation:\n", new_pop)
    return new_pop


def cross_over(population, c):
    for i in range(0, len(population) - 1, 2):
        if (i / 2) % 2 == 0:
            for j in range(c):
                population[i][j], population[i + 1][j] = population[i + 1][j], population[i][j]
        else:
            for j in range(len(population[0]) - 1, c, -1):
                population[i][j], population[i + 1][j] = population[i + 1][j], population[i][j]
    # print("Crossed Population:\n", population)
    return population


def mutation(population, m, mrate):
    mrate = mrate / 100
    for i in range(len(population)):
        select = random.random()
        if select < mrate:
            for j in range(m):
                rand_s = random.randint(1, 4)
                rand_j = random.randint(0, len(population[0]) - 1)
                population[i][rand_j] = rand_s
    # print("Mutated Population:\n", population)
    return population


n = 3  # size of board
fn = 6  # number of food
s = 12  # number of step
p = 4  # population
c = 4  # cutting point
m = 1  # mutation size
mrate = 50  # mutation rate percent
# start point indexes
x = 2
y = 2
board = np.zeros((n, n), dtype=int)
foods = generate_food(n, fn, x, y)
board = place_foods(board, foods)
population = np.random.randint(1, 5, size=(p, s))
board[x][y] = 8

# print(population)
# print(board)

print("Board:\n", board)
counter = 0
while True:
    population, fit_pop = work(board, population, fn, x, y)
    # print("population:\n", population)
    # print("normal", fit_pop)
    counter += 1
    print(counter)
    print(fit_pop)
    if 1 in fit_pop:
        print("Found it!")
        break
    # print("yüzdelik", calculate_fit(fit_pop))
    population = selection(population, calculate_fit(fit_pop))
    population = cross_over(population, c)
    population = mutation(population, m, mrate)
    print()
print("Board:\n", board)
print("Finding Way:", population[fit_pop.index(1)])
print("Counter=", counter)
plt.show()
