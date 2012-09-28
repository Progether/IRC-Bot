
class BehaviourModule:
    def __init__(self):
        self.behaviourList = list()

    def performBehaviours(self, data):
        for behaviour in self.behaviourList:
            behaviour.perform(data)

