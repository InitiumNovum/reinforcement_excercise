from unittest import TestCase
from wumpusWorld.Bayes import Bayes

class TestBayes(TestCase):
    def setUp(self) -> None:
        self.prob = Bayes.Probability(0.5)
#    def tearDown(self) -> None:
#        self.prob.dispose()

    def test_get(self):
        self.assertEqual(self.prob.x(), 0.5)

    def test_get(self):
        self.prob.x = 0.3
        self.assertEqual(self.prob.x, 0.3)
