import numpy as np
import random as r
import more_itertools as mit
import heapq as h
import statistics as s
from matplotlib import pyplot as plt

#genetic
n = 8 #size of vector in n-queen problem
population_size = 100 #size of population
generations_max = 1000 #number of generations
pc = 0.7 # crossing probality
pm = 0.5 # mutation probality

def generateFirstPopulation(chessboard_size, number_of_elements):
    population = []
    for a in range(number_of_elements):
        index = 0
        for b in range(chessboard_size):
            vector = mit.random_permutation(range(chessboard_size))
            index += 1
        #print(vector)
        vector = list(vector)
        population.append(vector)
    return population

def conflicts(state):#less is better
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                conflicts += 1
    #less conflicts = bigger priority
    #conflicts = n * n - conflicts
    return conflicts

def evaluateAttacks(population):
    number_of_attacks = []
    for a in range(len(population)):
        value = conflicts(population[a])
        number_of_attacks.append(value)
    return number_of_attacks

def sortPopulationByAttacks(population, attacksList):
    pr_queue = []
    result = []
    for a in range(len(population)):
        h.heappush(pr_queue, (attacksList[a], population[a]))
    for b in range(len(population)):
        value = pr_queue.pop()
        result.append(value[1])
    result.reverse()
    return result

def tourneySelection(population):
    #select from 2 random indexes better ones to crosing
    #one could be chosen multiple times
    selected = []
    for a in range(len(population)):
        first = r.randint(0, len(population)-1)
        sec = r.randint(0, len(population)-1)
        leftVeLessConflicts = (conflicts(population[first])) < (conflicts(population[sec]))
        if (leftVeLessConflicts):
            selected.append(population[first])
        else:
            selected.append(population[sec])
    return selected

def crossPopulation(population):
    newpopulation=[]
    n = len (population[0])

    for a in range(int(len(population)/2)):
        first = population[2 * a]
        sec = population[2 * a +1]
        #print("1 parent", first)
        #print("2 parent", sec)
        vector1 = []
        vector1.extend(first[:int(n/2)])
        vector1.extend(sec[int(n/2): n])
        newpopulation.append(vector1)
        vector2 = []
        vector2.extend(sec[:int(n/2)])
        vector2.extend(first[int(n/2): n])
        newpopulation.append(vector2)
        #print("1 child", (vector1))
        #print("2 child", vector2)
    return newpopulation

def Mutation(population, prob):
    for a in range(len(population)):
        rand = r.randint(0, len(population)-1) # probability of mutation happen on single entity
        if (rand > prob * len(population)):
            randindex = r.randint(0, n-1)
            randnr = r.randint(0, n-1)
            population[a][randindex] = randnr
            #print(f"random happend in {a} element on {randindex} index comes {randnr} nr")
    return population

'''Start of genetic algorithm'''
mean_list = []
champ_conflicts = []
generations = 1

a = generateFirstPopulation(n, population_size)
print("first population: ", a)

b = evaluateAttacks(a)
print("minimal colision", min(b))
champ_conflicts.append(min(b))

mean = s.mean(b)
print("Mean of 1st population: ", mean)
mean_list.append(mean)

#sorted = sortPopulationByAttacks(a, b)
#print("sorted population by attacks", sorted)

pop = 2
while (generations_max-1 > 0):

    # it brings just winners in random
    a = tourneySelection(a)
    #print("Selected to cross: ", a)

    a = crossPopulation(a)
    #print("new crossed Population: ", a)

    a = Mutation(a, pm)
    #print("after mutation", a)
    generations += 1

    b = evaluateAttacks(a)
    champ_conflicts.append(min(b))

    mean = s.mean(b)
    #print(f"Mean of {pop} population : ", mean)
    mean_list.append(mean)

    generations_max -= 1
    pop += 1

plt.plot(range(generations), mean_list)
plt.plot(range(generations), champ_conflicts, ".")
plt.title("mean of conflicts in next populations")
plt.xlabel("generations")
plt.ylabel("mean of conflicts")
plt. show()

a = sortPopulationByAttacks(a, b)
print("result: ", a[0])