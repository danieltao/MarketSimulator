from abc import abstractmethod
from market import generate_order


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
        self.money += delta
    
    def update_share(self, delta):
        self.shares += delta

class Fool(Agent):
    def __init__(self, id):
        super().__init__("fool", id)
    
    def propose(self, prices):
        share = 1
        if prices[-2] < prices[-1]:
            return generate_order(prices[-1], 'buy', self, share)
        else:
            return generate_order(prices[-1], 'sell', self, share)

def generate_agent(id):
    return Fool(id)
