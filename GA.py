# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 11:44:54 2018

@author: k4-tamura
"""
#Genetic Algorythm

#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.


#    example which maximizes the sum of a list of integers
#    each of which can be 0 or 1

##使う乱数の読み込み
import random
import math
##deapの読み込み
from deap import base
from deap import creator
from deap import tools

##どういうGAの問題にするか
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

##個体を作る
toolbox = base.Toolbox()
##初期化する方法
toolbox.register("attr_bool", random.randint, 0, 1)
##toolbox.attr_boolを100回繰り返し(Repeat)てえられるリストを個体(Individual)の属性とする。
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, 6)
#個体の集合をpopulationとする。
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#評価関数の定義
#indovidualは0,1で構成されるリストなので、その和が評価関数。
def evalOneMax(individual):
    s=0
    t=0
    for x in range(len(individual)):
        s += x*individual[x]
        #t += (individual[x]-0.2)*(individual[x]-0.2)
    return s,

#----------
# 操作のための理解
#----------
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.8)
toolbox.register("select", tools.selTournament, tournsize=5)

#----------

def main():
    random.seed(60)
    pop = toolbox.population(n=5)
    CXPB, MUTPB = 0.5, 0.2
    
    print("Start of evolution")
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0
    
    # Begin the evolution
    while g < 1:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        print(offspring)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        #offspring2 = [toolbox.clone(ind) for ind in (offspring,offspring)]
        print(offspring)
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            #print(ind.fitness.values)      
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        #offspring = tools.selTournament(offspring,tournsize=100,k=2)
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    print("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()
