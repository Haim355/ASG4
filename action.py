from persistence import *

import sys


def main(args: list[str]):
    inputfilename: str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: list[str] = line.strip().split(", ")
            action_prod_id, quantity, activ_id, date = splittedline

            quant = repo.products.find(id=action_prod_id)[0]
            quantity = int(quantity)

            if quantity > 0:
                repo.activities.insert(Activitie(action_prod_id, quantity, activ_id, date))
                repo.products.update({"quantity": quant.quantity + quantity}, {
                    "id": quant.id
                })
            elif int(quant.quantity) >= abs(quantity):
                repo.activities.insert(Activitie(action_prod_id, quantity, activ_id, date))
                repo.products.update({"quantity": quant.quantity - abs(quantity)}, {
                    "id": quant.id
                })


if __name__ == '__main__':
    main(sys.argv)