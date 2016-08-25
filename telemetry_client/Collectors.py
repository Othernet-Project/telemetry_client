class Collectors():
    def __init__(self, items, values=None):
        self.collectors = {}
        for key_name in items.keys():
            value = None
            if values and values.has_key(key_name):
                value = values[key_name]
            collector_type = items[key_name]
            self.collectors[key_name] = collector_type(value)

    def update(self, values):
        for key_name in self.collectors.keys():
            if values.has_key(key_name):
                self.collectors[key_name].update(values[key_name])

    def peek(self):
        r = {}
        for key_name in self.collectors.keys():
            r[key_name] = self.collectors[key_name].peek()
        return r

    def get(self):
        r = {}
        for key_name in self.collectors.keys():
            r[key_name] = self.collectors[key_name].get()
        return r
        
        
class Collector():
    def __init__(self, v=None):
        self.value = None
        if v is not None:
            self.update(v)

    def update(self,v):
        self.value = v

    def peek(self):
        return self.value

    def get(self):
        r = self.peek()
        self.__init__()
        return r

class AvgCollector(Collector):
    def __init__(self, v=None):
        self.value = 0
        self.count = 0
        if v is not None:
            self.update(v)

    def update(self,v):
        self.count += 1
        self.value += v

    def peek(self):
        if self.count > 0:
            return (1.0*self.value)/self.count
        else:
            return 0

class HistoCollector(Collector):
    def __init__(self, v=None):
        self.value = {}
        if v is not None:
            self.update(v)

    def update(self,v):
        if not self.value.has_key(v):
            self.value[v] = 0
        self.value[v] += 1


class LastCollector(Collector):
    pass

class SumCollector(Collector):
    def __init__(self, v=None):
        self.value = 0
        if v is not None:
            self.update(v)

    def update(self,v):
        self.value += v
