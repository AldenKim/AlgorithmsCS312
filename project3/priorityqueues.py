class LinearPQ:
    def __init__(self, distances):
        self.queue = {}
        for i in range(len(distances)):
            self.queue[i] = distances[i]

    def is_empty(self):
        return len(self.queue) == 0

    def pop_min(self):
        key, priority = min(self.queue.items(), key=lambda item: item[1])
        del self.queue[key]
        return key

    def update_priority(self, key,new_priority):
        self.queue[key] = new_priority


class HeapPQ:
    def __init__(self, distances):
        self.heap_tree = []
        for i in range(len(distances)):
            self.heap_tree.append((i, distances[i]))

        self.find_items = {}
        for i in range(len(distances)):
            self.find_items[i] = i

        #then percolate up to make complete tree
        for i in range(len(distances)-1, -1, -1):
            self.percolate_upward(i)

    def is_empty(self):
        if self.heap_tree:
            return False
        return True

    def pop_min(self):
        current_min = self.heap_tree[0][0]
        self.swap(0,len(self.heap_tree)-1)

        del self.heap_tree[len(self.heap_tree)-1]
        del self.find_items[current_min]

        #percolate downward
        self.percolate_downward(0)

        return current_min

    def update_priority(self, key, new_priority):
        if key not in self.find_items:
            return

        i = self.find_items[key]

        curr_priority = self.heap_tree[i][1]

        self.heap_tree[i] = (key, new_priority)

        if curr_priority > new_priority:
            #percolate upward
            self.percolate_upward(i)
        else:
            #percolate downward
            self.percolate_downward(i)

    def swap(self, first, second):
        item1 = self.heap_tree[first][0]
        item2 = self.heap_tree[second][0]

        self.find_items[item1] = second
        self.find_items[item2] = first

        temp = self.heap_tree[first]
        self.heap_tree[first] = self.heap_tree[second]
        self.heap_tree[second] = temp

    def percolate_upward(self, index):
        parent_i = index//2

        if parent_i < index and self.heap_tree[parent_i][1] > self.heap_tree[index][1]:
            self.swap(index, parent_i)
            self.percolate_upward(parent_i)

    def percolate_downward(self, index):
        left = index * 2 + 1
        right = index * 2 + 2

        change = index
        if left < len(self.heap_tree) and self.heap_tree[left][1] < self.heap_tree[index][1]:
            change = left

        if (right < len(self.heap_tree) and self.heap_tree[right][1] < self.heap_tree[index][1]
            and self.heap_tree[right][1] < self.heap_tree[left][1]):
            change = right

        if change == index:
            return

        self.swap(index, change)
        self.percolate_downward(change)
