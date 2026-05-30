class WorldEngine:
    def __init__(self):
        self.state = {
            "player_location": "grass",
            "player_backpack": [],
            "dangerous_level": 0,
            "fortune_level": 0,
            "hungry_level": 100,
            "animals": ["rabbit"],
            "items": [],
            "weather": "clear",
            "time": 1830,
        }

    def effect(self, event):
        pass

    def get_state(self):
        pass

class Summarizer:
    def __init__(self):
        pass

    def player_to_event(self, text, world_state):
        if "forest" in text:
            return {"type": "move", "target": "forest"}
        elif "grass" in text:
            return {"type": "move", "target": "grass"}
        elif "pick" in text:
            return {"type": "pick", "target": "rabbit"}

    def spirit_to_event(self, text):
        if "rain" in text:
            return {"type": "weather", "target": "rain"}
        elif "clear" in text:
            return {"type": "weather", "target": "clear"}

class SpiritAgent:
    def __init__(self, name):
        self.name = name
        self.character = ["cute", "Tsundere"]
        self.memory = []
        self.favor = 50
        self.max_chat_turns = 3
        self.language = "Chinese"

    def reply(self, world_summary, player_input):
        pass

class GameEngine:
    def __init__(self):
        self.world = WorldEngine()
        self.summarizer = Summarizer()
        self.spirit = SpiritAgent("Aliya")

    def run(self):
        while True:
            action = input(">")
            
    def save(self):
        pass

    def load(self):
        pass

