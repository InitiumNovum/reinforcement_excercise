class Bayes:
    class Probability:
        def __init__(self, x: float):
            self.x = x

        @property
        def x(self) -> float:
            return self._x

        @x.setter
        def x(self, x: float):
            if x < 0.0:
                self._x = 0.0
            elif x > 1.0:
                self._x = 1.0
            else:
                self._x = x
