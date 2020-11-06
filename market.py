
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
    executed_order_count, executed_total_money = 0, 0
    for si in range(len(sell_pile)):
        sell_order = sell_pile[si]
        sp, sc = sell_order["price"], sell_order['share']
        buy_order = buy_pile[bi]
        bp, bc = buy_order["price"], buy_order['share']
        while bp < sp:
            bi += 1
            buy_order = buy_pile[bi]
            bp, bc, bid = buy_order["price"], buy_order['share'], buy_order['id']
        sell_order['share'] -= min(sc, bc)
        buy_order['share'] -= min(sc, bc)
        execution_price = (sp + bp)/2
        executed_order_count += min(sc, bc)
        executed_total_money += min(sc, bc) * execution_price
        if sc > bc:
            bi += 1
        elif sc < bc:
            si += 1
        else:
            si, bi = si + 1, bi + 1


def cleanup_orders(orders):
    return orders
