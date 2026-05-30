class WorldEngine:
    def __init__(self):
        self.state = {
            player_location: "grass",
            player_backpack: [],
            dangerous_level: 0,
            fortune_level: 0,
        }

    def apply(self, action):
        white_list = ["move", "attack", "do", "pick", "chat"]
        pass

class Summarizer:
    def __init__(self):
        pass

    def player_to_event(self, text: str, world_state: dict) -> dict:
        pass

    def spirit_to_event(self, text: str) -> dict:
        pass

class SpiritAgent:
    def __init__(self, name):
        self.name = name
        self.character = ["cute", "Tsundere"]
        self.memory = []
        self.favor = 50
        self.max_chat_turns = 3

    def reply(self, world_summary, player_input):
        pass

class GameEngine:
    def __init__(self):
        self.world = WorldEngine()
        self.summarizer = Summarizer()
        self.spirit = SpiritAgent("Aliya")

    def run(self, action):
        while True:
            break
            
    def save(self):
        pass

    def load(self):
        pass

