from market import generate_order, handle_orders, cleanup_orders
from agents import generate_agent

# potential improvements:
# 1. limit order
# 2. more strategies
# 3. change agent type. eg if lost 50k, switch from fool to conservative
# 4. fractional share

    
    
# generate agents
agent_list = []
for i in range(100):
    agent_list.append(generate_agent(i))

# start simulating
prices = [100, 111, 112, 114, 140]
for t in range(100):
    proposed_orders = []
    for agent in agent_list:
        order = agent.propose(prices)
        proposed_orders.append(order)
    handle_orders(proposed_orders)


agent_list[0].money -= 1
print(agent_list[1].money)