from abc import abstractmethod
import random


class Agent():
    def __init__(self, invest_type, id, money=10000, share=10):
        self.type = invest_type
        self.money = money
        self.shares = share
        self.id = id
        self.last_order_fulfilled = {}
        self.last_proposed_price = 0

    @abstractmethod
    def propose(self):
        pass

    def update_money(self, delta):
        self.money += delta
        assert(self.money >= 0), self.type + str(self.money) + "/" +str(self.last_proposed_price) + "/" +str(delta)
    
    def update_share(self, delta):
        assert(self.shares>=0) , self.type
        self.shares += delta
    
    def update_last_order(self, fulfilled):
        if not fulfilled:
            self.last_order_fulfilled = {}
        else:
            self.last_order_fulfilled = fulfilled

    def update_last_proposed_price(self, price):
        self.last_proposed_price = price



class Chaser(Agent):
    def __init__(self, id):
        super().__init__("Chaser", id)
    
    def propose(self, prices):
        share = generate_share(self.shares)
        base_price = prices[-1]
        delta = random.random() * 10
        if prices[-2] < prices[-1]:
            return generate_order(base_price, "buy", self, share, delta)
        return generate_order(base_price, 'sell', self, share, delta)

class Fundamental(Agent):
    def __init__(self, id):
        super().__init__('Fundamental', id)
        self.target_price = 400 + 200 * random.random()
    
    def propose(self, prices):
        share = generate_share(self.shares)
        base_price = prices[-1]
        delta = random.random() * 10
        # always buy when still has money and price is below target price
        if  (base_price + delta) < self.target_price:
            return generate_order(base_price, "buy", self, share, delta)
        # always sell all when price is greater than target
        if (base_price - delta) >= self.target_price:
            return generate_order(base_price, 'sell', self, share, delta)

class Bear(Agent):
    def __init__(self, id):
        super().__init__('Bear', id, share=5)

    def propose(self, prices):
        share = generate_share(self.shares)
        delta = random.random() * 10
        return generate_order(prices[-1], 'sell', self, share, delta)

class Speculator(Agent):
    def __init__(self, id):
        super().__init__('Speculator', id)
    
    def propose(self, prices):
        share = generate_share(self.shares)
        delta = random.random() * 10
        if prices[-2] >= prices[-1]:
            return generate_order(prices[-1], "buy", self, share, delta)
        if prices[-2] < prices[-1]:
            return generate_order(prices[-1], 'sell', self, share, delta)

def generate_agent(id, type_dict):
    type_dice = random.randint(0,len(type_dict) - 1)
    # if id%2 ==0:
    #     type_dice = 1
    # else:
    #     type_dice = 0
    return type_dict[type_dice](id)

def generate_order(price, action, agent, share, delta):
    if share == 0:
        return None
    if action == "sell":
        delta = -delta
    # if last order is not fulfilled and this turn is the same action
    if action in agent.last_order_fulfilled and not agent.last_order_fulfilled[action]:
        price = agent.last_proposed_price + delta

    # avoid negative money and negative share
    if action=='buy':
        price = min(price, agent.money / share)
    else:
        share = min(agent.shares, share)
    if price <=0:
        return None
    # update last proposed price and order
    agent.update_last_proposed_price(price)
    agent.update_last_order({action: False})
    return {"price": price, "action": action, 'agent': agent, 'share': share}

def generate_share(max_shares):
    return random.randint(0,max_shares)
