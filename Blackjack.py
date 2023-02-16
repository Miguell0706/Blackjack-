# Make a blackjack game, classes are Deck, Hand,Card, and Game. Game has two functions play and game, hand has 5 functions, init, draw, calculate value, check value, is_blackjack, display.
import random


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['Rank']} of {self.suit}"


class Deck():
    def __init__(self):
        self.cards = []
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        ranks = [
            {"Rank": "A", "Value": 11},
            {"Rank": "2", "Value": 2},
            {"Rank": "3", "Value": 3},
            {"Rank": "4", "Value": 4},
            {"Rank": "5", "Value": 5},
            {"Rank": "6", "Value": 6},
            {"Rank": "7", "Value": 7},
            {"Rank": "8", "Value": 8},
            {"Rank": "9", "Value": 9},
            {"Rank": "10", "Value": 10},
            {"Rank": "J", "Value": 10},
            {"Rank": "Q", "Value": 10},
            {"Rank": "K", "Value": 10},
        ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        if len(self.cards) > 0:
            for _ in range(number):
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand():
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.value = 0
        self.cards = []

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def get_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            card_value = card.rank["Value"]
            self.value += card_value
            if card.rank["Rank"] == "A":
                has_ace = True
        if self.value > 21 and has_ace:
            self.value -= 10
        return self.value

    def is_blackjack(self):
        return self.value == 21

    def display(self, show_dealer=False):
        print(f"""{"Dealer's" if self.dealer else "Your"} hand: """)
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not self.is_blackjack() and not show_dealer:
                print("hidden")
            else:
                print(card)
        if not self.dealer:
            print("Value:", self.get_value())
        elif self.dealer and show_dealer:
            print("Value:", self.get_value())


class Game():
    def __init__(self):
        self.player_wins = 0
        self.dealer_wins = 0
        self.ties = 0

    def play(self):
        game = 0
        games_to_play = ""
        while games_to_play not in range(1, 6):
            try:
                games_to_play = int(
                    input("Enter number of games to play between (1-5): "))
                if games_to_play not in range(1, 6):
                    print("Invalid input...")
            except:
                print("Invalid input...")
        while game < games_to_play:
            game += 1
            deck = Deck()
            deck.shuffle()
            player_hand = Hand()
            dealer_hand = Hand(dealer=True)
            player_hand.add_card(deck.deal(2))
            dealer_hand.add_card(deck.deal(2))
            print()
            print("_"*30)
            print(f"Game {game} of {games_to_play}")
            print("Dealer wins:", self.dealer_wins)
            print("Player wins:", self.player_wins)
            print("Ties:", self.ties)
            print("_"*30)
            player_hand.display()
            print()
            dealer_hand.display()
            if self.check_win(player_hand, dealer_hand):
                print()
                input("Press enter to continue...")
                continue
            choice = ""
            while choice not in ["s","stand"] and player_hand.get_value() < 21:
                choice = input("Enter (H)it or (S)tand: ").lower()
                if choice in ["h", "hit"]:
                    print()
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()
                elif choice not in ["s","stand"]:
                    print("Invalid input...")
                
            if self.check_win(player_hand, dealer_hand):
                print()
                input("Press enter to continue...")
                continue
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal(1))
            if self.check_win(player_hand, dealer_hand):
                print()
                input("Press enter to continue...")
                continue
            self.check_win(player_hand, dealer_hand,game_over=True)
            print()
            input("Press enter to continue...")
            continue
        print("Thanks for playing!😁")

    def check_win(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print()
                self.dealer_wins += 1
                print("You busted, you lose! 😥")
                return True

            elif dealer_hand.get_value() > 21:
                print()
                dealer_hand.display(show_dealer=True)
                self.player_wins += 1
                print("Dealer busted, you win! 😀")
                return True

            elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
                print()
                dealer_hand.display(show_dealer=True)
                self.ties += 1
                print("Two blackjacks, a tie!😐 ")
                return True

            elif player_hand.is_blackjack():
                print()
                self.player_wins += 1
                print("You have blackjack, you win! 😀")
                return True

            elif dealer_hand.get_value() > 21:
                print()
                dealer_hand.display(show_dealer=True)
                self.dealer_wins += 1
                print("Dealer has blackjack, you lose! 😥")
                return True
            return False

        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print()
                dealer_hand.display(show_dealer=True)
                self.player_wins += 1
                print("You were closer to 21, you win!😀")
            elif player_hand.get_value() < dealer_hand.get_value():
                print()
                dealer_hand.display(show_dealer=True)
                self.dealer_wins += 1
                print("Dealer was closer to 21, you lose!😥")
            else:
                print()
                dealer_hand.display(show_dealer=True)
                self.ties += 1
                print("Equal values, a tie! 😐")
            return True


g = Game()
g.play()
