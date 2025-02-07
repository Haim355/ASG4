from persistence import *

def main():
    print("Activities")
    listofactivies = repo.activities.find_all()
    for activity in listofactivies:
        print(activity)
    print("Branches")
    listofbranches = repo.branches.find_all()
    for branch in listofbranches:
        print(branch)
    print("Employees")
    listofemployees = repo.employees.find_all()
    for employee in listofemployees:
        print(employee)
    print("Products")
    listofproducts = repo.products.find_all()
    for product in listofproducts:
        print(product)
    print("Suppliers")
    listofsuppliers = repo.suppliers.find_all()
    for supplier in listofsuppliers:
        print(supplier)

    print("\n")
    repo.printworkers()
    print("\n")

    repo.printActions()

if __name__ == '__main__':
    main()