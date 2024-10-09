class ArrayPQ:
    def __init__(self, distances):
        self.queue = {}
        for i in range(len(distances)):
            self.queue[i] = distances[i]

    def is_empty(self):
        if self.queue:
            return False
        return True

    def pop_min(self):
        key, priority = min(self.queue.items(), key=lambda item : item[1])
        del self.queue[key]
        return key

    def update_priority(self, key,new_priority):
        self.queue[key] = new_priority

    def insert(self, key, priority):
        self.queue[key] = priority


class HeapPQ:
    def __init__(self, distances):
        self.heap_tree = []
        for i in range(len(distances)):
            self.heap_tree.append((i, distances[i]))

        self.find_items = {}
        for i in range(len(distances)):
            self.find_items[i] = i

        #then percolate up to make complete tree

    def is_empty(self):
        if self.heap_tree:
            return False
        return True

    def pop_min(self):
        current_min = self.heap_tree[0][0]
        self.swap(0,-1)

        del self.heap_tree[-1]
        del self.find_items[current_min]

        #percolate downward

        return current_min

    def update_priority(self, key, new_priority):
        i = self.find_items[key]

        curr_priority = self.heap_tree[i][1]

        self.heap_tree[i] = (key, new_priority)

        if curr_priority > new_priority:
            #percolate upward
            return
        else:
            #percolate downward
            return

    def insert(self, key, new_priority):
        self.find_items[key] = len(self.heap_tree)

        self.heap_tree.append((key, new_priority))

        #percolate up


    def swap(self, first, second):
        item1 = self.heap_tree[first][0]
        item2 = self.heap_tree[second][0]

        self.find_items[item1] = second
        self.find_items[item2] = first

        temp = self.heap_tree[first]
        self.heap_tree[first] = self.heap_tree[second]
        self.heap_tree[second] = temp
