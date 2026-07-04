import json
import datetime
from pathlib import Path

from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    customers = [Customer(data) for data in config["customers"]]
    shops = [Shop(data) for data in config["shops"]]
    fuel_price = config["FUEL_PRICE"]
    distance = 0
    best_shop = None
    price_ride = 0

    for index, customer in enumerate(customers):
        if index > 0:
            print()

        print(f"{customer.name} has {customer.money} dollars")

        min_total_cost = 1000000
        best_shop = None

        for shop in shops:
            distance = (
                               (customer.location[0] - shop.location[0]) ** 2
                               + (customer.location[1] - shop.location[1]) ** 2
                       ) ** 0.5
            price_ride = (
                    customer.car.fuel_consumption / 100 * distance * fuel_price
            )

            current_total_cost = (
                    price_ride * 2
                    + customer.product_cart["milk"] * shop.products["milk"]
                    + customer.product_cart["bread"] * shop.products["bread"]
                    + customer.product_cart["butter"] * shop.products["butter"]
            )

            print(
                f"{customer.name}'s trip to the {shop.name} "
                f"costs {current_total_cost:.2f}"
            )

            if current_total_cost < min_total_cost:
                min_total_cost = current_total_cost
                best_shop = shop

        if min_total_cost > customer.money:

            print(
                f"{customer.name} doesn't have enough money "
                f"to make a purchase in any shop"
            )
        else:
            customer.location = best_shop.location
            customer.money -= min_total_cost

            date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            milk_cost = (
                    customer.product_cart["milk"] * best_shop.products["milk"]
            )
            bread_cost = (
                    customer.product_cart["bread"] * best_shop.products["bread"]
            )
            butter_cost = (
                    customer.product_cart["butter"] * best_shop.products["butter"]
            )
            total_prod_cost = (
                    customer.product_cart["milk"] * best_shop.products["milk"]
                    + customer.product_cart["bread"] * best_shop.products["bread"]
                    + customer.product_cart["butter"] * best_shop.products["butter"]
            )

            print(f"{customer.name} rides to {best_shop.name}\n")
            print(f"Date: {date_str}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print(f"You have bought:")
            print(
                f"{customer.product_cart['milk']} milks for "
                f"{int(milk_cost) if milk_cost.is_integer() else milk_cost} dollars"
            )
            print(
                f"{customer.product_cart['bread']} breads for "
                f"{int(bread_cost) if bread_cost.is_integer() 
                else bread_cost} dollars"
            )
            print(
                f"{customer.product_cart['butter']} butters for "
                f"{int(butter_cost) if butter_cost.is_integer() 
                else butter_cost} dollars"
            )
            print(
                f"Total cost is "
                f"{int(total_prod_cost) if total_prod_cost.is_integer() 
                else total_prod_cost} "
                f"dollars"
            )
            print("See you again!\n")
            print(f"{customer.name} rides home")
            print(f"{customer.name} now has {customer.money:.2f} dollars")
