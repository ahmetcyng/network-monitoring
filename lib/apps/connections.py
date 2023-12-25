class ConnectedSessions:
    def __init__(self):
        self.connections_list = []

    def add_connection(self, session):
        self.connections_list.append(session)

