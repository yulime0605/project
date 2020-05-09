from abc import ABCMeta, abstractmethod

class Card(metaclass=ABCMeta):
    suits = 'CDHS'
    ranks = '23456789TJQKA'

    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in Card.ranks or rank_suit[1] not in Card.suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")
    @property
    def rank(self):
        return self.card[0]

    @property
    def suit(self):
        return self.card[1]

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()


# ## Poker Card class
# 단, Poker game에서 두 카드를 비교할 때 suit과 무관하게 rank로만 결정한다. 오름차 순서로 나열하면 다음과 같다. 
# 
#     '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
# 
# Q. `Card` class를 상속받아 Poker game용 `PKCard` class를 정의하라. 
# >Hint: 위 순서대로 정수를 return하는 value() method를 implementation해야 한다.

# In[14]:


class PKCard(Card):
    
    def value(self):
        b=dict(zip(Card.ranks, range(2, 2+len(Card.ranks))))
        return b[self.card[0]]


if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')
    print(f'{c1} {c2} {c3}')

    # comparison
    print(c1 > c2 == c3)

    # sorting
    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards)


import random
class Deck:
    def __init__(self, cls):
        suits = 'CDHS'
        ranks = '23456789TJQKA'
        self.cards=[PKCard(x+y) for x in ranks for y in suits]
        
        
        
    def shuffle(self):
        random.shuffle(self.cards)
    def pop(self):
        a=self.cards[-1]
        del self.cards[-1]
        return a
    def __str__(self):
        return '{}'.format(self.cards)
    def __len__(self):
        return len(self.cards)
    def __getitem__(self,index):
        return self.cards[index]

if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)
