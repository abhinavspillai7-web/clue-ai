class knowledge_base:
    def __init__(self):
        self.facts=[]
        self.possible_owners={}
        self.constraints={}
        self.conclusions={}
        self.reasons={}
    def add_fact(self,facts):
        self.facts.append(facts)
kb = knowledge_base()
kb.add_fact("Test fact")
print(kb.facts)