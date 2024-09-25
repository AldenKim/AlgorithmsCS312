# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point
class Node:
    def __init__(self, point: tuple[float, float]):
        self.point = point
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, point: tuple[float, float]):
        newNode = Node(point)

        if self.head is None:
            newNode.next = newNode
            newNode.prev = newNode
            self.head = newNode
            self.tail = newNode
        else:
            self.tail = self.head.prev
            self.tail.next = newNode
            newNode.prev = newNode
            newNode.next = self.head
            self.head.prev = newNode

    def remove(self, node: Node):
        if node == self.head and self.head == self.tail:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node == self.head:
                self.head = node.next

def brute_force_points():



def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    if len(points) < 3:
        #brute force it

    return []
