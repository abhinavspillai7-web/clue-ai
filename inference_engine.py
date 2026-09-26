class InferenceEngine:
    def __init__(self,knowledge_base):
        self.kb=knowledge_base
    def process_fact(self,fact):
        responder1 = fact.responder
        suggested_cards1 = fact.suggested_cards
        if fact.response == "could_not_disprove":
            for i in suggested_cards1:
                self.kb.eliminate_owners(i,responder1)
            
