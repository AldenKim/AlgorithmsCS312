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
        self.queue = {}
