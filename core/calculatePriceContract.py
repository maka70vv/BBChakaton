def calculate_price(prices):
    total_price = 0
    price = ""
    counter = 0

    for i in prices:
        if i.isnumeric():
            price += i
        else:
            counter += 1

        if counter == 2:
            total_price += int(price)
            price = ""
            counter = 0

    return total_price
