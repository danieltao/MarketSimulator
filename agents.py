from abc import abstractmethod
import random


class Agent():
    def __init__(self, invest_type, id, money=1000, share=10):
        self.type = invest_type
        self.money = money
        self.shares = share
        self.id = id
        self.last_order_fulfilled = False

    @abstractmethod
    def propose(self):
        pass

    def update_money(self, delta):
        assert(self.money >= 0), self.type + str(self.money)
        self.money += delta
    
    def update_share(self, delta):
        assert(self.shares>=0) , self.type
        self.shares += delta
    
    def update_last_order(self, fulfilled):
        self.last_order_fulfilled = fulfilled


class Speculator(Agent):
    def __init__(self, id):
        super().__init__("Speculator", id)
    
    def propose(self, prices):
        share = 1
        base_price = prices[-1]
        delta = random.random() * 10
        if prices[-2] < prices[-1] and self.money>= (base_price + delta) * share:
            return generate_order(base_price, "buy", self, share, delta)
        elif self.shares >= share:
            return generate_order(base_price, 'sell', self, share, delta)

class Fundamental(Agent):
    def __init__(self, id):
        super().__init__('Fundamental', id, money=1000)
        self.target_price = 100 + 100 * random.random()
        print(self.target_price)
    
    def propose(self, prices):
        share = 1
        base_price = prices[-1]
        delta = random.random() * 10
        # always buy when still has money and price is below target price
        if self.money >= (base_price + delta) * share and (base_price + delta) < self.target_price:
            return generate_order(base_price, "buy", self, share, delta)
        # always sell all when price is greater than target
        if self.shares > 0 and (base_price - delta) >= self.target_price:
            return generate_order(base_price, 'sell', self, self.shares, delta)

class Bears(Agent):
    def __init__(self, id):
        super().__init__('bears', id, share=100)

    def propose(self, prices):
        share = 1
        delta = random.random() * 10
        if self.shares > 0:  
            return generate_order(prices[-1], 'sell', self, share, delta)


def generate_agent(id):
    if id % 10== 0:
        return Bears(id)
    elif id % 5 == 0:
        return Fundamental(id)
    else:
        return Speculator(id)

def generate_order(price, action, agent, share, delta):
    if action == "sell":
        delta = -delta
    if agent.last_order_fulfilled:
        price -= delta
    else:
        price += delta
    return {"price": price, "action": action, 'agent': agent, 'share': share}


