from utility import distance
from random import randint

class Customer:                             
    def __init__(self, x, y, demand=0): #creates new node to represent customer
        self.x = x
        self.y = y
        self.demand = demand


class Vehicle:
    def __init__(self, x, y): #node to represent the ants
        self.x = x
        self.y = y
        self.route = []
        self.visited = set()


class Depot:
    def __init__(self, x, y):
        self.x = x
        self.y = y



nodes = [
    Depot(500, 500),                           
    Customer(300, 400, demand=10), #create a new list that contains all nodes ranging from depot (starting point) to the customer node, demand represents the importance of said node, 
    Customer(400, 400, demand=5), #if a node is bigger, its importance is higher
    Customer(500, 300, demand=8),
    Customer(600, 400, demand=3),
    Customer(500, 400, demand=2),
    Customer(400, 500, demand=6),
    Customer(500, 600, demand=7),
    Customer(600, 500, demand=9),
    ]

# Create distance matrix for faster distance calculations
distance_matrix = [[distance(node1, node2)
                    for node2 in nodes] for node1 in nodes]


#function to calculate total distance
def calculate_total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1))

'''
how calculate_total_distance(route) works:

for index in range(length(route) - 1):
    return distance = math.sqrt((route[i].x - route[i+1].x) ** 2 + (route[i].y - route[i+1].y) ** 2)

    sum(distance) #for every distance between route sum all the routes



'''