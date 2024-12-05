import random

class card:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def toString(self):
        return f"Type: {self.type}, Value: {self.value}"

class croupier:
    def __init__(self):
        self.deck = []
        self.diamonDeck = []
        self.heartsDeck = []
        self.clubsDeck = []
        self.spadesDeck = []
        self.arrays_mini = [[] for _ in range(13)]


        for i in range(1, 14):  # Del 1 al 13
            self.heartsDeck.append(card("hearts", i))
            self.diamonDeck.append(card("diamonds", i))
            self.clubsDeck.append(card("clubs", i))
            self.spadesDeck.append(card("spades", i))

    def init_deck(self):
        self.deck = []  # Asegúrate de que 'deck' está vacío.
        types = [self.heartsDeck, self.diamonDeck, self.clubsDeck, self.spadesDeck]
        for deck_type in types:
            self.deck.extend(deck_type)
        self.shuffle()

    def shuffle(self):
        if not self.deck:
            print("La baraja está vacía. No se puede barajar.")
            return

        shuffle_count = random.randint(5, 10)
        
        for _ in range(shuffle_count):

            mid = len(self.deck) // 2
            first_half = self.deck[:mid]
            second_half = self.deck[mid:]
            self.deck = [] 


            while first_half or second_half:
                if first_half:
                    num_from_first = random.randint(1, min(len(first_half), 4))
                    for _ in range(num_from_first):
                        if first_half:  
                            self.deck.append(first_half.pop(0))

                if second_half:
                    num_from_second = random.randint(1, min(len(second_half), 4))
                    for _ in range(num_from_second):
                        if second_half:  
                            self.deck.append(second_half.pop(0))

    def posicionate(self):
        counter = 0
        for i in range(len(self.deck)):
            self.arrays_mini[counter].append(self.deck[i])
            counter += 1
            if counter == 13:
                counter = 0

    def card_game(self):
        
        pass

    def imprimir_grupos(self):
        for i in range(len(self.arrays_mini)):
            print(f"Array {i}:")
            for card in self.arrays_mini[i]:
                print(card.toString())
        print("")
        

def main():
    dealer = croupier() 
    dealer.init_deck()  

    dealer.posicionate()

    dealer.card_game()
if __name__ == "__main__":
    main()
