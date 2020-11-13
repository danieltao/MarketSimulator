from abc import abstractmethod
import random


class Agent():
    def __init__(self, invest_type, id, money=10000, share=10):
        self.type = invest_type
        self.money = money
        self.shares = share
        self.id = id
        self.last_order_fulfilled = False

    @abstractmethod
    def propose(self):
        pass

    def update_money(self, delta):
        assert(self.money >= 0)
        self.money += delta
    
    def update_share(self, delta):
        assert(self.shares>=0)
        self.shares += delta
    
    def update_last_order(self, fulfilled):
        self.last_order_fulfilled = fulfilled


class Speculator(Agent):
    def __init__(self, id):
        super().__init__("fool", id)
    
    def propose(self, prices):
        share = 1
        rand_delta = 5 + random.random() * 5
        base_price = prices[-1]
        if prices[-2] < base_price and self.money>= (base_price - rand_delta) * share:
            return generate_order_from_last(self.last_order_fulfilled, base_price, rand_delta, share, self, "buy")
        elif self.shares >= share:
            return generate_order_from_last(self.last_order_fulfilled, base_price, -rand_delta, share, self, "sell")

class Goodman(Agent):
    def __init__(self, id):
        super().__init__('goodman', id, money=20000)
    
    def propose(self, prices):
        share = 1
        base_price = prices[-1]
        rand_delta = 5 + random.random() * 5
        if self.money >= base_price * share:
            return generate_order_from_last(self.last_order_fulfilled, base_price, rand_delta, share, self, "buy")

class Bears(Agent):
    def __init__(self, id):
        super().__init__('bears', id)

    def propose(self, prices):
        share = 1
        if self.shares > 0:
            return generate_order(prices[-1], 'sell', self, share)


def generate_agent(id):
    if id % 2== 0:
        return Speculator(id)
    else:
        return Goodman(id)

def generate_order(price, action, agent, share):
    return {"price": price, "action": action, 'agent': agent, 'share': share}


def generate_order_from_last(last_order_fulfilled, base_price, delta, share, agent, buy_or_sell):
    if last_order_fulfilled:
        return generate_order(base_price - delta, buy_or_sell, agent, share)
    else:
        return generate_order(base_price + delta, buy_or_sell, agent, share)

