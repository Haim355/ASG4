import sqlite3
import atexit
from dbtools import Dao
 
# Data Transfer Objects:
class Employee(object):
    def __init__(self,id,name,salary,branche):
        self.id = id
        self.name = name
        self.salary = salary
        self.branche = branche

 
class Supplier(object):
    def __init__(self,id,name,contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

class Product(object):
    def __init__(self,id,description,price,quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Branche(object):
    def __init__(self,id,location,number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Activitie(object):
    def __init__(self,product_id,quantity,activator_id,date):
        self.product_id = product_id
        self.quantity=quantity
        self.activator_id = activator_id
        self.date =date

 
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.employees= Dao(Employee,self._conn)
        self.suppliers= Dao(Supplier,self._conn)
        self.branches=Dao(Branche,self._conn)
        self.activities=Dao(Activitie,self._conn)
        self.products=Dao(Product,self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()

    def printworkers(self):
        print("Employees report")

        script = """
        SELECT e.name, 
               e.salary, 
               b.location, 
               IFNULL(SUM(p.price * ABS(a.quantity)), 0) AS total_sales
        FROM employees AS e
        JOIN branches AS b ON e.branche = b.id
        LEFT JOIN activities AS a ON e.id = a.activator_id AND a.quantity < 0
        LEFT JOIN products AS p ON a.product_id = p.id
        GROUP BY e.id
        ORDER BY e.name;
        """

        results = self.execute_command(script)

        for row in results:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]}")

    def printActions(self):
        print("Activities report")

        script = """
        SELECT a.date, 
               p.description, 
               a.quantity, 
               e.name AS seller, 
               s.name AS supplier
        FROM activities AS a
        JOIN products AS p ON a.product_id = p.id
        LEFT JOIN employees AS e ON a.activator_id = e.id AND a.quantity < 0
        LEFT JOIN suppliers AS s ON a.activator_id = s.id AND a.quantity > 0
        ORDER BY a.date;
        """

        results = self.execute_command(script)

        for row in results:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")


# singleton
repo = Repository()
atexit.register(repo._close)