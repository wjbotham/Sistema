class Agent:
    def __init__(self,name,body):
        self.name = name
        self._body = body
        body.add_agent(self)

    def get_body(self):
        return self._body
    def set_body(self,body):
        body.remove_agent(self)
        self._body = body
        body.add_agent(self)
    body = property(get_body,set_body)

    def teleport(self,destination):
        self.body = destination
