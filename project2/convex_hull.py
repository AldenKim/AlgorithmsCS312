# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point
import sys

import plotting as plot

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

    #case where our line is completely vertical
    if x1 == x2:
        return None, x1

    m = (y2 - y1) / (x2 - x1)
    b = y1 - (m * x1)
    return m, b

#implement the brute force algorithm given in slides
def brute_force_points(points: list[tuple[float, float]]):
    hull = set()
    n = len(points)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            p1 = points[i]
            p2 = points[j]

            m, b = find_line(p1, p2)
            above = 0
            below = 0

            for k in range(n):
                if k == i or k == j:
                    continue
                point = points[k]

                #First if is case for vertical lines
                if m is None:
                    if point[0] > b:
                        above += 1
                    elif point[0] < b:
                        below += 1
                else:
                    y = m * point[0] + b
                    if point[1] > y:
                        above += 1
                    elif point[1] < y:
                        below += 1

            if above == 0 or below == 0:
                hull.add(p1)
                hull.add(p2)

    return list(hull)

#helper function1 for tangent
def slope(p1: tuple[float, float], p2: tuple[float, float]):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        return None

    m = (y2 - y1) / (x2 - x1)
    return m

#helper function2 for tangent
def right_most(left: DoublyLinkedList):
    if left.head is None:
        return None

    current = left.head
    right_most_point = current

    while True:
        if current.point[0] > right_most_point.point[0]:
            right_most_point = current
        current = current.next
        if current == left.head:
            break

    return right_most_point

#Tangent and merging stuff
def find_upper_tangent(left: DoublyLinkedList, right: DoublyLinkedList):
    p = right_most(left)
    q = right.head

    done = 0

    #plot.draw_line(p.point, q.point, color="red")
    while not done:
        done = 1

        while slope(p.point, q.point) > slope(p.prev.point, q.point):
            p = p.prev
            done = False
            #plot.draw_line(p.point, q.point, color="red")

        while slope(q.point, p.point) < slope(q.next.point, p.point):
            q = q.next
            done = False
            #plot.draw_line(p.point, q.point, color="red")

    return p.point, q.point

def find_lower_tangent(left: DoublyLinkedList, right: DoublyLinkedList):
    p = right_most(left)
    q = right.head

    done = 0
    #plot.draw_line(p.point, q.point, color="red")
    while not done:
        done = 1

        while slope(p.point, q.point) < slope(p.next.point, q.point):
            p = p.next
            done = False
            #plot.draw_line(p.point, q.point, color="red")
        
        while slope(q.point, p.point) > slope(q.prev .point, p.point):
            q = q.prev
            done = False
            #plot.draw_line(p.point, q.point, color="red")
        
    return p.point, q.point

def merge(left: DoublyLinkedList, right: DoublyLinkedList):
    p1, q1 = find_upper_tangent(left, right)
    p2, q2 = find_lower_tangent(left, right)

    #plot.draw_line(p1,q1, color = "red")
    #plot.draw_line(p2, q2, color="red")
    mergedLinkedList = DoublyLinkedList()

    current = left.head
    while current.point != p2:
        current = current.next

    while current.point != p1:
        mergedLinkedList.insert(current.point)
        current = current.next
    mergedLinkedList.insert(current.point)

    current = right.head
    while current.point != q1:
        current = current.next

    while current.point != q2:
        mergedLinkedList.insert(current.point)
        current = current.next
    mergedLinkedList.insert(current.point)

    return mergedLinkedList.convert_to_list()

def helper(left_most_point: tuple[float, float], point: tuple[float, float]):
    sl = slope(left_most_point, point)
    return sl is None, sl

def sort_by_slope(left_most_point: tuple[float, float], points: list[tuple[float, float]]):
    sorted_points = sorted(points, key=lambda k: helper(left_most_point, k), reverse=True)
    return sorted_points

#Actual function
def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    #base case
    if len(points) <= 3:
        #brute force it
        return brute_force_points(points)

    #Greater than three points, do below
    points.sort()

    #Split into 2 sub problems, find convex hull of left half and right half
    mid = len(points) // 2
    left_points = compute_hull(points[:mid])
    right_points = compute_hull(points[mid:])

    left_min = sys.maxsize
    right_min = sys.maxsize
    left_min_i = 0
    right_min_i = 0

    for i in range(len(left_points)):
        if left_points[i][0] < left_min:
            left_min = left_points[i][0]
            left_min_i = i

    for i in range(len(right_points)):
        if right_points[i][0] < right_min:
            right_min = right_points[i][0]
            right_min_i = i

    #sort left_points by clockwise order
    left_points = sort_by_slope(left_points[left_min_i], left_points)
    #sort right_points by clockwise order
    right_points = sort_by_slope(right_points[right_min_i], right_points)

    left = DoublyLinkedList()
    right = DoublyLinkedList()

    #Using new data structure to help us
    for point in left_points:
        left.insert(point)

    for point in right_points:
        right.insert(point)

    #merging/tangent stuff
    return merge(left, right)
