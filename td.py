import pandas as pd

class Player:
    def __init__(self, name: str, rating: float) -> None:
        self.name = name
        self.rating = rating
        self.score = 0
        self.color_balance = 0
        self.record = {}
    
    def already_played(self, player: str):
        return player in self.record.keys()
    
    def info(self) -> dict:
        return {
            "name": self.name,
            "rating": self.rating,
            "score": self.score
        }

class Bye(Player):
    def __init__(self) -> None:
        super().__init__("Bye", 0)

class Tournament:
    def __init__(self) -> None:
        self.players = []
        self.standings = []
        self.round = 1
    
    def add_player(self, new_player: Player) -> None:
        for player in self.players:
            if new_player.name == player.name:
                raise ValueError("This player has already been entered into the tournament.")
        self.players.append(new_player)
        self.update_standings()

    def sort_players(self) -> None:
        for attr in ('rating', 'score'): #Sorting order
            self.players.sort(key=lambda player: player.__dict__[attr], reverse=True)
       
    def update_standings(self):
        self.sort_players()
        self.standings = [player.info() for player in self.players]
        self.table = pd.DataFrame(self.standings)
    
    def pair(self) -> None:
        num = len(self.players)
        if num < 2: raise ValueError("Needs atleast two players.")
        if num % 2 == 1: self.players.append(Bye())
        self.update_standings()

        scoretables = []
        for score in sorted(self.table.score.value_counts().index.tolist(), reverse=True):
            scoretables.append((self.table.loc[self.table['score'] == score]))
        
        for i in range(len(scoretables) - 1):
            if len(scoretables[i]) % 2 == 1:
                scoretables[i] = scoretables[i].append(scoretables[i + 1].iloc[[0]])
                scoretables[i + 1] = scoretables[i + 1].iloc[1:]
                if scoretables[i + 1].empty: scoretables.pop(i + 1)

        #print(scoretables)
        pairings = []
        for scoretable in scoretables:
            names = list(scoretable['name'])
            midpoint = int((len(names) + 1)/2)
            upper_section = names[:midpoint]
            lower_section = names[midpoint:]
            for i in range(len(upper_section)):
                pairings.append((upper_section[i], lower_section[i]))
        
        print(pairings)

if __name__ == "__main__":
    import random
    t = Tournament()
    players = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    for i in range(len(players)):
        p = Player(players[i], random.randint(1000, 2900))
        p.score = random.randint(0, 5)
        t.add_player(p)
    print(t.table)
    t.pair()
    