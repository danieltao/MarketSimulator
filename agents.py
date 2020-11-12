from abc import abstractmethod
import random


class Agent():
    def __init__(self, invest_type, id, money=10000, share=10):
        self.type = invest_type
        self.money = money
        self.shares = share
        self.id = id

    @abstractmethod
    def propose(self):
        pass

    def update_money(self, delta):
        assert(self.money >= 0)
        self.money += delta
    
    def update_share(self, delta):
        assert(self.shares>=0)
        self.shares += delta

class Fool(Agent):
    def __init__(self, id):
        super().__init__("fool", id)
    
    def propose(self, prices):
        share = 1
        rand_delta = random.random() * 5
        if prices[-2] < prices[-1] and self.money>= (prices[-1] - rand_delta) * share:
            return generate_order(prices[-1] - rand_delta, 'buy', self, share)
        elif self.shares >= share:
            return generate_order(prices[-1] + rand_delta, 'sell', self, share)

class Goodman(Agent):
    def __init__(self, id):
        super().__init__('goodman', id, money=20000)
    
    def propose(self, prices):
        share = 2
        if self.money >= prices[-1] * share:
            return generate_order(prices[-1], 'buy', self, share)

class Bears(Agent):
    def __init__(self, id):
        super().__init__('bears', id)

    def propose(self, prices):
        share = 1
        if self.shares > 0:
            return generate_order(prices[-1], 'sell', self, share)


def generate_agent(id):
    if id % 2== 0:
        return Fool(id)
    else:
        return Goodman(id)

def generate_order(price, action, agent, share):
    return {"price": price, "action": action, 'agent': agent, 'share': share}
