class World:
    def __init__(self):
        self.state = {
            "location": "grass",
            "dangerous": 0,
            "items": ["medicine"],
            "animals": ["rabbit"]
        }

    def action(self, action):
        if action == "move to forest":
            self.state["location"] = "forest"
            self.state["dangerous"] = 5
        elif action == "move to river":
            self.state["location"] = "river"
            self.state["dangerous"] = 2
        elif action == "hunt rabbit":
            self.state["items"].append("rabbit meat")
            self.state["animals"].remove("rabbits")
            self.state["dangerous"] = 0
        else:
            print("Invalid action")

    def summary(self):
        return f"at {self.state['location']}, dangerous {self.state['dangerous']}, there are {self.state['animals']} and {self.state['items']}"

class Spirit:
    def __init__(self, name):
        self.memory = []
        self.favor = 50

    def reply(self, world_summary, player_input):
        self.memory.append(f"player_input: {player_input}")
        self.memory.append(f"world_summary: {world_summary}")
        return f"you just say go to {player_input}, now we are {world_summary}, what should we do?"

world = World()
spirit = Spirit("Aliya")

# print(world.summary())

# world.action("move to forest")  
# print(world.summary())

# world.action("hunt rabbits")
# print(world.summary())

while True:
    p = input("chat:").strip()
    if p in ["q", "quit"]:
        print("saving...")
        break
    
    action = ""
    if "forest" in p:
        action = "move to forest"
    elif "river" in p:
        action = "move to river"
    else:
        action = "chat"
    
    world.action(action)
    env = world.summary()
    r = spirit.reply(env, p)
    print(f"Aliya:{r}")
