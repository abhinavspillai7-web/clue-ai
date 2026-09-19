from datetime import datetime
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
    def __init__(self,fact_id,suggestor,responder,suggested_cards,response,shown_card,timestamp):
        self.fact_id=fact_id
        self.suggestor=suggestor
        self.responder=responder
        self.suggested_cards=suggested_cards
        self.response=response
        self.shown_card=shown_card
        self.timestamp=timestamp
    def __repr__(self):
        return f"fact id:{self.fact_id},suggestor:{self.suggestor},reponder:{self.responder}"
kb = knowledge_base()
fact1=Fact(1,"alice","bob",{"alice","bob","charlie"},"could_not_disprove",None,datetime.now())        
kb.add_fact(fact1)
print(kb.facts)