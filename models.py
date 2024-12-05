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

        # Inicializar las cartas de cada tipo
        for i in range(1, 14):  # Del 1 al 13
            self.heartsDeck.append(card("hearts", i))
            self.diamonDeck.append(card("diamonds", i))
            self.clubsDeck.append(card("clubs", i))
            self.spadesDeck.append(card("spades", i))

    def init_shuffle(self):
        types = [self.heartsDeck, self.diamonDeck, self.clubsDeck, self.spadesDeck]
        random.shuffle(types)  # Mezclar los tipos de mazos para mayor aleatoriedad

        self.deck = []
        counter = 0

        while counter < 52:
            # Seleccionar un tipo de mazo aleatorio
            current_type = random.choice(types)

            # Determinar cuántas cartas sacar del mazo (máximo restante y máximo 4)
            max_cards = min(len(current_type), 4, 52 - counter)
            
            # Validar si hay cartas disponibles en este mazo
            if max_cards <= 0:
                continue  # Pasar al siguiente mazo si este está vacío

            cant = random.randint(1, max_cards)

            # Mover las cartas seleccionadas al mazo general
            for _ in range(cant):
                self.deck.append(current_type.pop())

            counter += cant

        # Mezclar la baraja general al final
        random.shuffle(self.deck)

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


def main():
    dealer = croupier() 
    dealer.init_shuffle()  

    print("Cartas en la baraja inicializada:")
    for card in dealer.deck:
        print(card.toString())
    print("")
    dealer.shuffle() 

    print("Cartas en la baraja barajada:")
    for card in dealer.deck:
        print(card.toString())
    print("")
if __name__ == "__main__":
    main()
