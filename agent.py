class Agent:

    def __init__(self, agent_id: int):
        self.id = agent_id

    def __str__(self):
        return str(f'agent_{self.id}')

    def __hash__(self):
        return self.id

    def __eq__(self, other: 'Agent'):
        return self.id == other.id

    def __repr__(self):
        return self.__str__()
