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

    def convert_to_list(self):
        values = []
        if self.head is None:
            return values

        value = self.head
        while True:
            values.append(value.point)
            value = value.next
            if value == self.head:
                break
        return values
#Code for our data structure


#helper function to help us find slope and intercept of two points
def find_line(p1: tuple[float, float], p2: tuple[float, float]):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        return None, x1

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b

#implement the brute force algorithm given in slides
def brute_force_points(points: list[tuple[float, float]]):
    hull = []
    n = len(points)
    for i in range(n):
        for j in range(n):
            p1 = points[i]
            p2 = points[j]

            m, b = find_line(p1, p2)

            count = 0

            for point in points:
                if m is None:
                    if point[0] > b:
                        count += 1
                else:
                    if point[1] > (m * point[0]) + b:
                        count += 1

            if count == n or count == 0:
                if p1 not in hull:
                    hull.append(p1)
                if p2 not in hull:
                    hull.append(p2)

    return hull

def cross_product(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def find_upper_tangent(left: DoublyLinkedList, right: DoublyLinkedList):
    p = left.tail
    q = right.head

    done = 0

    while not done:
        done = 1

        while cross_product(p.point, q.point, p.prev.point) > 0:
            p = p.prev
            done = False

        while cross_product(q.point, p.point, q.next.point) < 0:
            q = q.next
            done = False

    return p.point, q.point

def find_lower_tangent(left: DoublyLinkedList, right: DoublyLinkedList):
    p = left.tail
    q = right.head

    done = 0
    while not done:
        done = 1

        while cross_product(p.point, q.point, p.prev.point) < 0:
            p = p.prev
            done = False
        
        while cross_product(q.point, p.point, q.next.point) > 0:
            q = q.next
            done = False
        
    return p.point, q.point


def merge(left: DoublyLinkedList, right: DoublyLinkedList):
    p1, q1 = find_upper_tangent(left, right)
    p2, q2 = find_lower_tangent(left, right)

    mergedLinkedList = DoublyLinkedList()


    return


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    #base case
    if len(points) <= 3:
        #brute force it
        return brute_force_points(points)

    #Greater than three points
    points.sort()

    mid = len(points) // 2
    left_points = compute_hull(points[:mid])
    right_points = compute_hull(points[mid:])

    left = DoublyLinkedList()
    right = DoublyLinkedList()

    #Using new data structure to help us
    for point in left_points:
        left.insert(point)

    for point in right_points:
        right.insert(point)


    #merging/tangent stuff
    merge(left, right)

    return []
