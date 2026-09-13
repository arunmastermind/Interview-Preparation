class BatchIterator:
    def __init__(self, items, batch_size):
        self.items = items
        self.batch_size = batch_size
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration
        batch = self.items[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        return batch

for batch in BatchIterator(list(range(10)), 3):
    print(batch)