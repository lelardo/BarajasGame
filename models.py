import random

class card: # Clase que representa una carta de la baraja
    def __init__(self, type, value):
        self.type = type #simbolo de carta (corazones, diamantes, tréboles, picas)
        self.value = value # valor o numero de la carta

    def toString(self): # Método que retorna un string con la información de la carta
        return f"Simbolo: {self.type}, Valor: {self.value}"

class croupier:
    def __init__(self):
        self.deck = [] # Baraja de cartas (baraja general) 
        self.diamonDeck = [] # Baraja de diamantes
        self.heartsDeck = [] # Baraja de corazones
        self.clubsDeck = [] # Baraja de tréboles
        self.spadesDeck = [] # Baraja de picas
        self.arrays_mini = [[] for _ in range(13)] # pequeños arrays de 4 cartas, simulan los grupos de 4 cartas en el juego

        for i in range(1, 14):  # inicializa las cartas de la baraja sin ponerlas en ella
            self.heartsDeck.append(card("hearts", i)) # crea las cartas de corazones
            self.diamonDeck.append(card("diamonds", i)) # crea las cartas de diamantes
            self.clubsDeck.append(card("clubs", i)) # crea las cartas de tréboles
            self.spadesDeck.append(card("spades", i)) # crea las cartas de picas

    def init_deck(self):
        self.deck = [] # vacia la baraja porsiacaso
        types = [self.heartsDeck, self.diamonDeck, self.clubsDeck, self.spadesDeck] # tipos de cartas
        for deck_type in types: # recorre los tipos de cartas
            self.deck.extend(deck_type) # añade las cartas al mazo general
        self.shuffle() # baraja la baraja segun nuestro metodo

    def shuffle(self): # Método que baraja la baraja humanamente
        if not self.deck: # si la baraja está vacía, no se puede barajar
            print("La baraja está vacía. No se puede barajar.")
            return # termina la función

        shuffle_count = random.randint(5, 10) # cantidad de veces que se barajará la baraja
        
        for _ in range(shuffle_count): # baraja la baraja shuffle_count veces

            mid = len(self.deck) // 2 # divide la baraja en dos
            first_half = self.deck[:mid] # primera mitad de la baraja
            second_half = self.deck[mid:] # segunda mitad de la baraja
            self.deck = [] # vacía la baraja para volver a rellenarla

            while first_half or second_half: # mientras haya cartas en alguna de las mitades
                if first_half: # para la primera mitad
                    num_from_first = random.randint(1, min(len(first_half), 4)) # cantidad de cartas que se sacarán de la primera mitad
                    for _ in range(num_from_first): # por cada carta que se sacará
                        if first_half:  # si hay cartas en la primera mitad
                            self.deck.append(first_half.pop(0)) # saca la carta de la primera mitad y la añade a la baraja

                if second_half: # para la segunda mitad
                    num_from_second = random.randint(1, min(len(second_half), 4)) # cantidad de cartas que se sacarán de la segunda mitad
                    for _ in range(num_from_second): # por cada carta que se sacará
                        if second_half: # si hay cartas en la segunda mitad
                            self.deck.append(second_half.pop(0)) # saca la carta de la segunda mitad y la añade a la baraja

    def posicionate(self): # Método que posiciona las cartas en los grupos de 4 cartas
        counter = 0 # contador para saber en qué grupo de 4 cartas se está
        for i in range(len(self.deck)): # recorre la baraja
            self.arrays_mini[counter].append(self.deck[i]) # añade la carta al grupo de 4 cartas correspondiente
            counter += 1 # aumenta el contador
            if counter == 13: # si el contador llega a 13
                counter = 0 # reinicia el contador

    def card_game(self):
        aux_end = 0  # Contador para verificar si todos los grupos están completos
        act_array = 12  # Empezamos en el último grupo (13 - 1)
        control = [0 for _ in range(13)]  # Control para saber cuántas cartas tiene cada grupo

        while True:
            # Verifica si ya no hay cartas en el grupo actual
            if not self.arrays_mini[act_array]:
                print(f"El grupo {act_array} está vacío. No hay más cartas para mover. ¡Has perdido!")
                break

            # Obtén la carta actual del grupo activo
            act_card = self.arrays_mini[act_array].pop(0)  # Tomamos la carta de la cabeza del grupo actual
            print(f"Carta actual: {act_card.toString()}")  # Imprime la carta que estamos jugando

            # Calcula el índice del siguiente grupo
            next_array = act_card.value - 1

            # Verifica si el grupo de destino ya está lleno (4 cartas)
            if control[next_array] == 4:
                print(f"El grupo {next_array} ya está completo. ¡No puedes mover más cartas! ¡Has perdido!")
                break

            # Mueve la carta al grupo correspondiente
            self.arrays_mini[next_array].append(act_card)

            # Actualiza el contador del grupo
            control[next_array] += 1
            if control[next_array] == 4:  # Si un grupo tiene 4 cartas completas
                aux_end += 1
                print(f"Grupo {next_array} completo.")

            # Verifica si se han completado todos los grupos
            if aux_end >= 13:  # Si todos los grupos tienen 4 cartas
                print("¡Todos los grupos están completos! ¡Has ganado!")
                break

            # Actualiza el grupo activo
            act_array = next_array

            # Verifica si ya no hay cartas en ningún grupo excepto en el activo
            if all(len(group) == 0 for i, group in enumerate(self.arrays_mini) if i != act_array):
                print("No hay más cartas disponibles en otros grupos. ¡Has perdido!")
                break

            # Imprime el estado actual de los grupos
            self.imprimir_grupos()

    def imprimir_grupos(self): # Método que imprime los grupos de 4 cartas
        for i in range(len(self.arrays_mini)): # recorre los grupos de 4 cartas
            print(f"Array {i}:") # imprime el número de grupo
            for card in self.arrays_mini[i]: # recorre las cartas del grupo
                print(card.toString()) # imprime la carta
        print("")
        

def main():
    dealer = croupier() 
    dealer.init_deck()  
    dealer.shuffle()
    dealer.posicionate()
    dealer.card_game()
if __name__ == "__main__":
    main()