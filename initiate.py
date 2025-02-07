from persistence import *

import sys
import os

def add_branche(splittedline : list[str]):
    branche_id, branche_loc, branch_numofemp = splittedline
    repo.branches.insert(Branche(branche_id, branche_loc, branch_numofemp))


def add_supplier(splittedline : list[str]):
    supp_id,supp_name,supp_contactinfo = splittedline
    repo.suppliers.insert(Supplier(supp_id, supp_name, supp_contactinfo))


def add_product(splittedline : list[str]):
    id,desc,quant,price = splittedline
    repo.products.insert(Product(id, desc, quant, price))


def add_employee(splittedline : list[str]):
    empid,empname,empsala,empbranch = splittedline
    repo.employees.insert(Employee(empid, empname, empsala, empbranch))


adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    repo._close()
    if os.path.isfile("bgumart.db"):
        os.remove("bgumart.db")
    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)