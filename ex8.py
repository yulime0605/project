class Set:
    def __init__(self, value = []):    # Constructor
        self.data = []                 # Manages a list
        self.concat(value)

    def intersection(self, other):        # other is any sequence
        res = []                       # self is the subject
        for x in self.data:
            if x in other:             # Pick common items
                res.append(x)
        return Set(res)                # Return a new Set

    def union(self, other):            # other is any sequence
        res = self.data[:]             # Copy of my list
        for x in other:                # Add items in other
            if not x in res:
                res.append(x)
        return Set(res)

    def concat(self, value):
        for x in value:                
            if not x in self.data:     # Removes duplicates
                self.data.append(x)

    def __len__(self):          return len(self.data)        # len(self)
    def __getitem__(self, key): return self.data[key]        # self[i], self[i:j]
    def __and__(self, other):   return self.intersection(other) # self & other
    def __or__(self, other):    return self.union(other)     # self | other
    def __repr__(self):         return 'Set({})'.format(repr(self.data))  
    def __iter__(self):         return iter(self.data)       # for x in self:

    def issubset(self, other):
        for i in self.data:
            if i in other.data:
                continue
            else:
                return False       

        return True
    def __le__(self, other):                  # <=
        if self.issubset(other)==True:
            return True
        return False
    def __lt__(self, other):                    # <
        if self.issubset(other)==True:
            if len(self.data)!= len(other.data):
                return True 
        return False

    def issuperset(self, other):
        for i in other.data:
            if i in self.data:
                continue
            else:
                return False  
        return True  
    
    def __ge__(self, other):                # >=
        if self.issuperset(other)==True:
            return True
        return False
    def __gt__(self, other):                # >
        if self.issuperset(other)==True:
            if len(self.data)!= len(other.data):
                return True
        return False

    def __ior__(self,other):
        for i in other.data:
            if i not in self.data:
                self.data.append(i)
        return Set(self)

    def intersection_update(self, other):
        for i in self.data:
            if i not in other.data:
                self.data.remove(i)
        return Set(self)



    def __iand__(self, other):
        for i in self.data:
            if i not in other.data:
                self.data.remove(i)
        return Set(self)
         

    def difference_update(self, other):
        for i in self.data:
            if i in other.data:
                self.data.remove(i)
        return Set(self)

    def __isub__(self, other):
        for i in self.data:
            if i in other.data:
                self.data.remove(i)
        return Set(self)


    def symmetric_difference_update(self, other):
        for i in self.data:
            if i in other.data:
                self.data.remove(i)
        for z in other.data:
            if z not in self.data:
                self.data.append(z)

        return Set(self)
        
    def add(self,elem):
        self.data.append(elem)
        return Set(self)

    def remove(self,elem):
        if elem in self.data:
            self.data.remove(elem)
        return Set(self)
