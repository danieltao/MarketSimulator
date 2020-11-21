from market import handle_orders, cleanup_orders, calculate_price
from agents import generate_agent, Speculator, Chaser, Fundamental, Bear
import matplotlib.pyplot as plt
from collections import Counter
from scipy import stats
import numpy as np

# potential improvements:
# 1. limit order
# 2. more strategies
# 3. change agent type. eg if lost 50k, switch from fool to conservative
# 4. fractional share
# 8. right now the money is always asserted to be above 0 (no debt)
# 10. trader --- liquidity
# 11. partially imperfect


def calculate_utility(prices, agent):
    start_utility = 10000 + 10*414/2
    end_utility = agent.money + agent.shares * prices[-1] /2
    return end_utility - start_utility

def plot(prices):
    # analysis
    plt.plot(prices)
    plt.xlabel('time')
    plt.ylabel('price')
    plt.show()

def simulate(type_dict):
    # generate agents
    agent_list = []
    for i in range(500):
        agent_list.append(generate_agent(i, type_dict))

    # start simulating
    prices = [414, 423, 422, 423, 420]
    for t in range(200):
        proposed_orders = []
        for agent in agent_list:
            order = agent.propose(prices)
            proposed_orders.append(order)
        # print(proposed_orders)
        # clean up last round order fulfilled bools
        orders, count, money = handle_orders(proposed_orders)
        # print(count)
        # orders = cleanup_orders(orders)
        calculate_price(prices, count, money)
        if prices[-1] <= 0:
            for agent in agent_list:
                agent.shares = 0
            break


    utilities = {"Speculator":0, 'Chaser':0, 'Bear':0, 'Fundamental':0}
    counter = {"Speculator":0, 'Chaser':0, 'Bear':0, 'Fundamental':0}
    total_stock = 0
    total_money = 0
    for agent in agent_list:
        utilities[agent.type] += calculate_utility(prices, agent)
        counter[agent.type] += 1
        total_stock += agent.shares
        total_money += agent.money
    for key in utilities:
        if counter[key] == 0:
            continue
        utilities[key] /= counter[key]
    # print(utilities, prices[-1])
    # plot(prices)
    return utilities

def determine_winner(utilities): 
    v=list(utilities.values())
    k=list(utilities.keys())
    return k[v.index(max(v))]

def calc_stats(array):
    mean = stats.tmean(array)
    std = stats.tstd(array)
    return std

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h, h

if __name__ == "__main__":    
    type_dict = {0: Chaser, 1: Speculator, 2: Bear, 3: Fundamental}
    # for i in range(3):
    #     type_dict[len(type_dict)] = Chaser
    # for i in range(13):
    #     type_dict[len(type_dict)] = Fundamental
    type_to_class = {"Speculator":Speculator, 'Chaser':Chaser, 'Bear':Bear, 'Fundamental':Fundamental}
    lines = {Speculator:[], Chaser:[], Bear:[], Fundamental:[]}
    for i in range(100):
        utilities = simulate(type_dict)
        # winner_type = determine_winner(utilities)
        # type_dict[len(type_dict)] = type_to_class[winner_type]
        # c = Counter(type_dict.values())
        for key in utilities:
            value = utilities[key]
            key = type_to_class[key]
            lines[key].append(value)
    c = Counter(type_dict.values())
    for key in c:
        print(key, c[key])
    # utilities = simulate(type_dict)
    # plt.plot(lines[Speculator], "r", label="Speculator")
    # plt.plot(lines[Chaser], 'b', label='Chaser')
    # plt.plot(lines[Bear], 'g', label='Bear')
    # plt.plot(lines[Fundamental], "k", label='Fundatmental')
    # plt.legend()
    # plt.show()
    for key in lines:
        print(key, calc_stats(lines[key]), mean_confidence_interval(lines[key]))
