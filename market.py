from agents import Agent


def handle_orders(orders):
    sell_pile, buy_pile = [], []
    for order in orders:
        if order:
            if order['action'] == "buy":
                buy_pile.append(order)
            else:
                sell_pile.append(order)
    buy_pile = sorted(buy_pile, key=lambda order: order['price'])
    sell_pile = sorted(sell_pile, key=lambda order: order['price'])
    highest_buy_price = buy_pile[-1]['price']
    bi, si = 0, 0
    executed_order_count, executed_total_money = 0, 0
    while si < len(sell_pile):
        sell_order = sell_pile[si]
        sp, sc, sagent = sell_order["price"], sell_order['share'], sell_order['agent']
        buy_order = buy_pile[bi]
        bp, bc, bagent = buy_order["price"], buy_order['share'], buy_order['agent']
        while bp < sp:
            bi += 1
            if bi == len(buy_pile):
                return orders, executed_order_count, executed_total_money
            buy_order = buy_pile[bi]
            bp, bc, bagent = buy_order["price"], buy_order['share'], buy_order['agent']
        delta_share = min(sc, bc)
        # update order
        sell_order['share'] -= delta_share
        buy_order['share'] -= delta_share
        # bookkeep price
        execution_price = (sp + bp)/2
        executed_order_count += delta_share
        executed_total_money += delta_share * execution_price

        # update agent shares and money
        bagent.update_share(delta_share)
        sagent.update_share(- delta_share)
        bagent.update_money(- delta_share * execution_price)
        sagent.update_money(delta_share * execution_price)
        
        # update last round order fulfilled
        bagent.update_last_order(True)
        sagent.update_last_order(True)

        if sc > bc:
            bi += 1
        elif sc < bc:
            si += 1
        else:
            si, bi = si + 1, bi + 1
        if bi == len(buy_pile):
            return orders, executed_order_count, executed_total_money

    return orders, executed_order_count, executed_total_money

def cleanup_orders(orders):
    new_orders = []
    for order in orders:
        if order['share'] > 0:
            new_orders.append(order)
    return new_orders

def calculate_price(prices, order_count, order_value):
    if order_count == 0:
        prices.append(prices[-1])
    else:
        prices.append(order_value/order_count)
