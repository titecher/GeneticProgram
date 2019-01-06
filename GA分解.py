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
    toolbox.attr_bool, 10)
#個体の集合をpopulationとする。
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#評価関数の定義
#indovidualは0,1で構成されるリストなので、その和が評価関数。
def evalOneMax(individual):
    s=0
    for x in range(len(individual)):
        s += individual[x]*(5-x)
    return s,

#----------
# 進化計算
#----------
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(640)
    
    pop = toolbox.population(n=5)
    #CXPB, MUTPB = 0.5, 0.2
    ##現状の集団を評価する
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    #fits = [ind.fitness.values[0] for ind in pop]
    
    offspring = toolbox.select(pop, len(pop))
    offspring = list(map(toolbox.clone, offspring))
    print("aaa",pop)
    print("bbb",offspring)
    #print(toolbox.clone)
    print("ccc",offspring[::2])
    print("ccc",offspring[1::2])
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    pop[:] = offspring
    print("aaa",pop)
        
if __name__ == "__main__":
    main()

