
class Cash:
    def __init__(self, n50, n20, n10, n5, c200, c100, c50, c20, c10, c5, c2,
                 c1):
        self.n50 = n50
        self.n20 = n20
        self.n10 = n10
        self.n5 = n5
        self.c200 = c200
        self.c100 = c100
        self.c50 = c50
        self.c20 = c20
        self.c10 = c10
        self.c5 = c5
        self.c2 = c2
        self.c1 = c1

    def valueOfCash(self):
        return self.n50 * 50 + self.n20 * 20 + self.n10 * 10 + self.n5 * 5 + self.c200 * 2 + self.c100 * 1 \
               + self.c50 * 0.5 + self.c20 * 0.2 + self.c10 * 0.1 + self.c5 * 0.05 + self.c2 * 0.02\
               + self.c1 * 0.01