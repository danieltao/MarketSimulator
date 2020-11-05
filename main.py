from abc import abstractmethod

# potential improvements:
# 1. limit order
# 2. more strategies
# 3. change agent type. eg if lost 50k, switch from fool to conservative
# 4. fractional share

class Agent():
    def __init__(self, invest_type, id, money=10000):
        self.type = invest_type
        self.money = money
        self.id = id

    @abstractmethod
    def propose(self):
        pass

    def update_money(self, delta):
        self.money += delta

class Fool(Agent):
    def __init__(self, id):
        super().__init__("fool", id)
    
    def propose(self, prices):
        share = 1
        if prices[-2] < prices[-1]:
            return generate_order(prices[-1], 'buy', id, share)
        else:
            return generate_order(prices[-1], 'sell', id, share)

def generate_agent(id):
    return Fool(id)

def generate_order(price, action, id, share):
    return {"price": price, "action": action, 'id': id, 'share': share}

def handle_orders(orders):
    sell_pile, buy_pile = [], []
    for order in orders:
        if order['action'] == "buy":
            buy_pile.append(order)
        else:
            sell_pile.append(order)
    buy_pile = sorted(buy_pile, key=lambda order: order['price'])
    sell_pile = sorted(sell_pile, key=lambda order: order['price'])
    bi, si = 0, 0
    for si in range(len(sell_pile)):
        sell_order = sell_pile[si]
        sp, sc, sid = sell_order["price"], sell_order['share'], sell_order['id']
        buy_order = buy_pile[bi]
        bp, bc, bid = buy_order["price"], buy_order['share'], buy_order['id']
        while bp < sp:
            bi += 1
            buy_order = buy_pile[bi]
            bp, bc, bid = buy_order["price"], buy_order['share'], buy_order['id']
        sell_order['share'] -= min(sc, bc)
        buy_order['share'] -= min(sc, bc)
        execution_price = (sp + bp)/2
        if sc > bc:
            bi += 1
        elif sc < bc:
            si += 1
        else:
            si, bi = si + 1, bi + 1



def cleanup_orders(orders):
    return orders

    

    
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