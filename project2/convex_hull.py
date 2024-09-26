# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point

#Code for our data structure
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
            tail = self.tail
            tail.next = newNode
            newNode.prev = tail
            newNode.next = self.head
            self.head.prev = newNode
            self.tail = newNode

    def remove(self, node: Node):
        if node == self.head and self.head == self.tail:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if node == self.head:
                self.head = node.next
#Code for our data structure

def find_line(p1: tuple[float, float], p2: tuple[float, float]):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        return None, x1

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b

def brute_force_points(points: list[tuple[float, float]]):
    hull = []
    n = len(points)
    for i in range(n):
        for j in range(n):
            p1 = points[i]
            p2 = points[j]

            m, b = find_line(p1, p2)

            count_above = 0
            count_below = 0

            for point in points:
                if m is None:
                    if point[0] > b:
                        count_above += 1
                    elif point[0] < b:
                        count_below += 1
                else:
                    y_line = m * point[0] + b
                    if point[1] > y_line:
                        count_above += 1
                    elif point[1] < y_line:
                        count_below += 1

            if count_above == 0 or count_below == 0:
                if p1 not in hull:
                    hull.append(p1)
                if p2 not in hull:
                    hull.append(p2)

    return hull

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    if len(points) < 3:
        #brute force it
        return brute_force_points(points)

    points.sort()

    return []
