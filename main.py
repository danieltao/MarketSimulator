from market import handle_orders, cleanup_orders, calculate_price
from agents import generate_agent
import matplotlib.pyplot as plt

# potential improvements:
# 1. limit order
# 2. more strategies
# 3. change agent type. eg if lost 50k, switch from fool to conservative
# 4. fractional share
# 8. right now the money is always asserted to be above 0 (no debt)
# 10. trader --- liquidity
# 11. partially imperfect


def calculate_utility(prices, agent):
    start_utility = 10000 
    end_utility = agent.money 
    return end_utility - start_utility


if __name__ == "__main__":    
    # generate agents
    agent_list = []
    for i in range(100):
        agent_list.append(generate_agent(i))

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
        print(count)
        # print(count)
        # orders = cleanup_orders(orders)
        calculate_price(prices, count, money)
        assert(prices[-1] > 0)

    print(prices)
    agent_list[0].money -= 1
    # analysis
    plt.plot(prices)
    plt.xlabel('time')
    plt.ylabel('price')
    plt.show()

    utilities = {"Speculator":0, 'Chaser':0, 'Bear':0, 'Fundamental':0}
    total_stock = 0
    total_money = 0
    for agent in agent_list:
        utilities[agent.type] += calculate_utility(prices, agent)
        print(calculate_utility(prices, agent))
        total_stock += agent.shares
        total_money += agent.money
    
    print(utilities)
    print(total_stock)
    print(total_money)

