class Agent:

    def __init__(self, agent_id: str):
        self.id = agent_id

    def __str__(self):
        return 'agent_' + self.id

    def __hash__(self):
        return int(self.id)

    def __eq__(self, other: 'Agent'):
        return self.id == other.id

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    agent = Agent("001")
    print(agent)
