class knowledge_base:
    def __init__(self):
        self.facts=[]
        self.possible_owners={}
        self.constraints={}
        self.conclusions={}
        self.reasons={}
    def add_fact(self,facts):
        self.facts.append(facts)
class Fact :
    def __init__(self,fact_id,suggestor,responder,suggested_cards,responder):
        self.fact_id=fact_id
        self.suggestor=suggestor
        self.responder=responder
        self.suggested_cards=suggested_cards
        self.responder=responder
kb = knowledge_base()
fact1=Fact(1,"alice","bob",{"alice","bob","charlie"},"could_not_disprove")        
kb.add_fact(fact1)
print(kb.facts)