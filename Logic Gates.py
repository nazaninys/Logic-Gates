from random import randrange
import random
import pandas as pd
from operator import attrgetter

class Chromosome():
    def __init__(self):
        self.genes = []
        self.fitness = 0

    def operation(self, op, first, second):
        if op == 0:
            return first & second
        if op == 1:
            return ~(first & second)
        if op == 2:
            return first | second
        if op == 3:
            return ~(first | second)
        if op == 4:
           return first ^ second
        if op == 5:
           return ~(first ^ second)
        
    def set_fitness(self, data):
        new = self.operation(self.genes[0], data.iloc[:,0], data.iloc[:,1])
        for i in range(2, len(data.columns) - 1):
            new = self.operation(self.genes[i - 1], new, data.iloc[:,i])
        ans = (data.iloc[:, -1] == new)
        self.fitness = ans.sum()



def initial_generation(generation, number, crowd):
    for i in range(crowd):
        chrom = Chromosome()
        for j in range(number):
            chrom.genes.append(randrange(6))
        generation.append(chrom)


def fitness(generation, data):
    for chrome in generation:
        chrome.set_fitness(data)

def select(generation, crowd):
    generation = sorted(generation, key=lambda x: x.fitness, reverse=False)
    new_gen = random.choices(generation, weights=[item ** 4 for item in range(len(generation))], k=crowd)
    return new_gen

def crossover(pars, crowd, number, data):
    prob = 0.8
    new_gen = []
    for i in range(20):
        chrome = Chromosome()
        for j in range(number):
            chrome.genes.append(randrange(6))
        pars.append(chrome)
    crowd += 20
    random.shuffle(pars)

    for i in range(crowd // 2):
        par1 = pars[i * 2]
        par2 = pars[i * 2 + 1]
        child1 = Chromosome()
        child2 = Chromosome()
        if random.random() < prob:
            point = randrange(number)

            for j in range(number):
                if j < point:
                    child1.genes.append(par1.genes[j])
                    child2.genes.append(par2.genes[j])
                else:
                    child1.genes.append(par2.genes[j])
                    child2.genes.append(par1.genes[j])
        else:
            child1.genes = par1.genes.copy()
            child2.genes = par2.genes.copy()

        new_gen.append(child1)
        new_gen.append(child2)
    delete_mins(new_gen, data)
    return new_gen


def delete_mins(new_gen, data):
    fitness(new_gen, data)
    for i in range(20):
        mini = min(new_gen, key=attrgetter('fitness'))
        new_gen.remove(mini)




def goal_test(generation, number):
    maxi = max(generation, key=attrgetter('fitness'))
    if maxi.fitness == 2 ** (number + 1):
        return False, maxi
    return True, maxi

def mutation(generation, crowd, prob, number):
    for i in range(crowd):
        if random.random() < prob:
            point = randrange(number)
            gate = randrange(6)
            generation[i].genes[point] = gate

def detect_gate(gate):
    if gate == 0:
        print('AND', end=' ')
    elif gate == 1:
        print('NAND', end=' ')
    elif gate == 2:
        print('OR', end=' ')
    elif gate == 3:
        print('NOR', end=' ')
    elif gate == 4:
        print('XOR', end=' ')
    elif gate == 5:
        print('XNOR', end=' ')


def print_answer(chrome):
    for gate in chrome.genes:
        detect_gate(gate)
    print()





file_name = 'truth_table.csv'
data = pd.read_csv(file_name)
generation = []
number = len(data.columns) - 2
crowd = 300
prob = 1/number
initial_generation(generation, number, crowd)
count = 0
result = [True, 0]


while (result[0]):
    if count % 10 == 0:
        if prob > 0.02:
            prob *= 0.9

    fitness(generation, data)
    pars = select(generation, crowd)
    generation = crossover(pars, crowd, number, data)
    mutation(generation, crowd, prob, number)
    count += 1
    result = goal_test(generation, number)
    print(count, result[1].fitness)

print_answer(result[1])
