# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:53:00 2018

@author: k4-tamura
"""
##一般ライブラリ
import random
import itertools
import math

##deapの読み込み
from deap import base
from deap import creator
from deap import tools

##deap
N = 10
dist = {}
point = {}

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

##個体を作る
toolbox = base.Toolbox()

toolbox.register("indices", random.sample, range(N), N)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#評価関数の定義
#移動距離の計算
def evalOneMax(individual):
    Length = 0
    for x in range(len(individual)-1):
        pair = [individual[x],individual[x+1]]
        pair.sort()
        #print(pair[0],pair[1],dist[pair[0],pair[1]])
        Length += dist[pair[0],pair[1]]
    #print(Length)
    return Length,

#----------
# 操作のための理解
#----------
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.8)
toolbox.register("select", tools.selTournament, tournsize=5)

#TSP用にルートを作る
def main():
    random.seed(64)
    #拠点数決める。

    #拠点位置を決める。
    base = []
    x = []
    y = []
    for i in range(N):
        base = base + [[i,(random.random(),random.random())]] 
        x = x + [base[i][1][0]]
        y = y + [base[i][1][1]]
    comb = list(itertools.combinations(base,2))
    print(comb)
    for i in range(len(comb)):
        dist[comb[i][0][0],comb[i][1][0]]=math.sqrt((comb[i][0][1][0]-comb[i][1][1][0])**2+(comb[i][0][1][1]-comb[i][1][1][1])**2)
    #拠点間距離を求める。
    
    import matplotlib.pyplot as plt
    
    plt.scatter(x, y, s=500)
    plt.legend()
    plt.show()
    
    ##Genetic Algorythm
    #問題設定    
    #交叉確率と変異確率
    MatP=0.5
    MutP=0.3
    #遺伝子の定義
    pop = toolbox.population(n=20)
    #最初の評価
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        
    fits = [ind.fitness.values[0] for ind in pop]
    cnt = 0
    
    #GA開始
    Competitor = pop
    while cnt < 100:
        cnt =cnt + 1
        #Competitor = toolbox.select(pop, len(pop))
        Competitor = list(map(toolbox.clone, Competitor))
        #交叉
        for cand1, cand2 in zip(Competitor[::2], Competitor[1::2]):
            if random.random() < MatP:
                toolbox.mate(cand1, cand2)
                del cand1.fitness.values
                del cand2.fitness.values
        #変異
        for mutant in Competitor:
            if random.random() < MutP:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        #再計算
        invalid_ind = [ind for ind in Competitor if not ind.fitness.valid]
        print(invalid_ind)
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            
        pop[:]=Competitor
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
        
        #統計情報
    
if __name__ == "__main__":
    main()