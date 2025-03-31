class Player():
    def __init__(self, name: str, money: int):
        self.name = name
        self.money = money
        self.hand = []
        self.current_bet = 0 
        self.fold = False
        self.all_in = False

    def get_cards(self, cards: list):
        self.hand = cards

    def bet(self, amount: int, min_bet: int, max_bet: int):
        if self.fold:
            raise ValueError("Already folded, cannot bet.")
        
        if amount < min_bet:
            raise ValueError("Need to bet more.")
        
        if amount > max_bet:
            raise ValueError("Need to bet less.")
        
        if amount > self.money:
            amount = self.money
        
        self.money -= amount
        self.current_bet += amount

        if self.money == 0:
            self.all_in = True

        return amount
    
    def fold(self):
        self.fold = True

    def reset(self):
        self.current_bet = 0
        self.all_in = False
        self.hand = []
        self.fold = False
        

        
    

        