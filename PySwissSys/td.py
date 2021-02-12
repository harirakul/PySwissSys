import pandas as pd
import pickle

class Player:
    def __init__(self, name: str, rating: float, uscf_id = None) -> None:
        self.name = name
        self.rating = rating
        self.score = 0
        self.uscf_id = uscf_id
        self.color_balance = 0
        self.record = []
    
    def __str__(self) -> str:
        return self.name
    
    def record_result(self, result: int, opponent) -> None:
        if result not in (1, 0.5, 0): raise ValueError
        self.record.append([result, opponent])
        self.score += result
        if result in (1, 0): 
            opponent.record.append([result ^ 1, self])
            opponent.score += result ^ 1
        else: 
            opponent.record.append([result, self]) #0.5
            opponent.score += result
    
    def already_played(self, player: str) -> bool:
        return player in sum(self.record, [])
    
    def info(self) -> dict:
        return {
            "Name": self,
            "USCF ID": self.uscf_id,
            "Rating": self.rating,
            "Score": self.score
        }

class Bye(Player):
    def __init__(self) -> None:
        super().__init__("Bye", 0)

class Tournament:
    def __init__(self, name = "Unnamed") -> None:
        self.players = []
        self.standings = []
        self.round = 1
        self.table = pd.DataFrame()
    
    @classmethod
    def load(cls, filename: str):
        with open(filename, 'rb') as f:
            cls = pickle.load(f)
        return cls
    
    def add_player(self, new_player: Player) -> None:
        for player in self.players:
            if new_player.name == player.name:
                raise ValueError("This player has already been entered into the tournament.")
        self.players.append(new_player)
        self.update_standings()

    def sort_players(self) -> None:
        for attr in ('rating', 'score'): #Sorting order
            self.players.sort(key=lambda player: float(player.__dict__[attr]), reverse=True)
       
    def update_standings(self):
        self.sort_players()
        self.standings = [player.info() for player in self.players]
        self.table = pd.DataFrame(self.standings)
        self.table.index += 1
    
    def pair(self) -> pd.DataFrame:
        num = len(self.players)
        if num < 2: raise ValueError("Needs atleast two players.")
        if num % 2 == 1: self.players.append(Bye())
        self.update_standings()

        scoretables = []
        for score in sorted(self.table["Score"].value_counts().index.tolist(), reverse=True):
            scoretables.append((self.table.loc[self.table['Score'] == score]))
        
        for i in range(len(scoretables) - 1):
            if len(scoretables[i]) % 2 == 1:
                scoretables[i] = scoretables[i].append(scoretables[i + 1].iloc[[0]])
                scoretables[i + 1] = scoretables[i + 1].iloc[1:]
                #if scoretables[i + 1].empty: scoretables.pop(i + 1)

        self.pairings = []
        print(scoretables)
        for scoretable in scoretables:
            names = list(scoretable['Name'])
            midpoint = int((len(names) + 1)/2)
            upper_section = names[:midpoint]
            lower_section = names[midpoint:]
            for i in range(len(upper_section)):
                #Optimize the selection for players' color
                L = [lower_section[i], lower_section[i].color_balance]
                R = [upper_section[i], upper_section[i].color_balance]

                best_move = 0
                best_score = 10

                for move in (-1, 1):
                    L[1] += move; R[1] -= move
                    if abs(L[1]) + abs(R[1]) < best_score:
                        best_score = abs(L[1]) + abs(R[1])
                        best_move = move
                    L[1] -= move; R[1] += move

                if best_move == -1:
                    pairing = [R[0], L[0]]
                    R[0].color_balance += 1
                    L[0].color_balance -= 1
                else:
                    pairing = [L[0], R[0]]
                    L[0].color_balance += 1
                    R[0].color_balance -= 1

                self.pairings.append(pairing)
        
        pairing_table = (pd.DataFrame(self.pairings))
        pairing_table.columns = ['White', 'Black']
        pairing_table.index.rename('Board', inplace=True)
        pairing_table.index += 1
        return pairing_table
    
    def record_results(self, results: list) -> None:
        #White Win: 1, Black Win: 0, Draw: 0.5
        if len(results) != len(self.pairings): raise ValueError
        for i in range(len(results)):
            self.pairings[i][0].record_result(results[i], self.pairings[i][1])
        self.round += 1
    
    def save(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    import random
    t = Tournament()
    players = list('ABCDEFGH')

    for i in range(len(players)):
        p = Player(players[i], random.randint(1000, 2900))
        t.add_player(p)

    print("=================TOURNAMENT================")
    print(t.table)

    for i in range(1, 5):
        print(f"=================ROUND {i}==================")
        print(t.pair())
        results = []
        for pairing in t.pairings:
            if pairing[0].rating > pairing[1].rating:
                results.append(1)
            else: results.append(0)
        t.record_results(results)
        t.update_standings()
        print(t.table)
    