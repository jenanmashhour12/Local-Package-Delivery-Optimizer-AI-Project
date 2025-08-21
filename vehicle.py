class Vehicle:
    def __init__(self, vid, capacity):
        self.id = vid
        self.capacity = capacity
        self.route = []    
        self.remaining_capacity = capacity
