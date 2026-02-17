import random
from protocol import OneTimePadProtocol

# Initialization
protocol = OneTimePadProtocol(n=1000, L=4028, d=40)

def test_scenarios(protocol, iterations=6000):
    wasted = {"a": [], "b": [], "c": []}
    parties_lst = list(protocol.parties.keys())
    
    for _ in range(iterations):
        # Scenario "a": One random party sends messages
        sender = random.choice(parties_lst)
        used_pads = set()
        for _ in range(protocol.n // 4):
            pad_index = random.choice(protocol.parties[sender])
            used_pads.add(pad_index)
        wasted["a"].append(len(used_pads))
        
        # Scenario "b": Two random parties send messages randomly
        senders = random.sample(parties_lst, 2)
        used_pads = set()
        for _ in range(protocol.n // 4):
            sender = random.choice(senders)
            pad_index = random.choice(protocol.parties[sender])
            used_pads.add(pad_index)
        wasted["b"].append(len(used_pads))
        
        # Scenario "c": Message sending among all parties
        probability = [random.random() for _ in range(4)]
        total = sum(probability)
        probability = [p / total for p in probability]
        used_pads = set()
        for _ in range(protocol.n // 4):
            sender = random.choices(parties_lst, probability)[0]
            pad_index = random.choice(protocol.parties[sender])
            used_pads.add(pad_index)
        wasted["c"].append(len(used_pads))
    
    return {k: round(sum(v)/len(v)) for k, v in wasted.items()}

# Run and print results
results = test_scenarios(protocol)
print("Average Wasted Pads:", results)