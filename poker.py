


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


# 위의 예에서 my_hand와 your_hand는 단순히 rank value가 가장 큰 것이 이긴다는 'high card' 족보만으로 따졌을 때이다. Poker의 패는 [List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)에서 보듯이 다양한 족보가 있다.
# 
# ## Poker Hands
# 지난 Programming Assignement를 object-oriented로 설계 구현해 보자.
# 
# [List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)의 Hand rank category 표에 열거된 패의 rank 0..9 을 역순으로 9..0의 integer로 나열하면 hand ranking의 높고 낮음을 알수 있다. 이 수를 혼동하지 않도록 이라 하자.
# 
# Straight, flush, straight flush와 같이 rank가 다른 5장으로 패가 이뤄지는 경우, 
# hand ranking이 같으면
# 1. 5장끼리 rank value를 비교해서 판단해야 한다. 즉, reverse(decreading) order로 sorting하여 rank value를 비교하면 된다.
# 
# Hand ranking이 같다면, 예를 들어 둘 다 two pair로 동률 이루고 있다면
# 1. 높은 수 one pair의 rank value를 비교하고
# 2. 같으면, 낮은 one pair의 rank value를 비교하고
# 3. 같으면, 나머지 1장 끼리 value를 비교해서 승부를 가른다. 
# 
# 따라서, 패가 이뤄지는지 찾는 method들은 (hand_ranking, five_cards) tuple로 return한다면
# tuple 비교하는 Python rule에 따라 행하면 충분하게 된다.
# 이때, 이어지는 five_cards는 rank가 높은 순서로 sorting하거나, rank가 같은 것이 있다면(find_a_kind의 경우)
# tie-breaking이 먼저 일어날 카드들을 앞으로 배치해야 list간 비교로 간편히 비교 가능히다. (four cards, tripple cards, high pair)
# 
# Q. *PA. Find poker hands* 문제에서 function으로 구현한 것들을 OOP로 rewriting하라.
# 
# 중요: hand ranking 찾기, hand ranking이 같을 때 tie-break이 제대로 적용되는지를 검증하기 위한
# 가능한 모든 test case를 20개 이상을 작성함으로써, unit test가 *거의* 모든 경우를 포함하고 있음을
# 보여야 한다.

# In[ ]:


class Hands():

    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards =sorted(cards,reverse=True)

    def is_flush(self):
        for i in range(4):
            if self.cards[i][1]!=self.cards[i+1][1]:
                return False
            else:
                continue
        return True

    def is_straight(self):
        ranks = '23456789TJQKA'
        values = dict(zip(ranks, range(2, 2+len(ranks))))
        hand_a=[(self.cards[i][1],values[self.cards[i][0]]) for i in range(5)]
        hand_b=sorted(hand_a,key=lambda x:x[1],reverse=True)
        for i in range(4):
            if hand_b[i][1]-1 != hand_b[i+1][1]:
                return None
            else:
                continue
        return hand_b

    def classify_by_rank(self):
        a=[self.cards[i][0] for i in range(5)]
        dict1={}
        for i in a:
            if not i in dict1:
                dict1[i]=a.count(i)
        if len(dict1)==5:
            return None
        else:
            return dict1

    def find_a_kind(self):
        cards_by_ranks = self.classify_by_rank()
        if cards_by_ranks!=None:
            b=sorted(cards_by_ranks.values(),reverse=True)
            if b[0]==4:
                name='four of a kind'
            elif b[0]==3:
                if b[1]==2:
                    name='full house'
                else:   
                    name='three of a kind'
            elif b[0]==2:
                if b[1]==2:
                    name='two pair'
                else:
                    name='one pair'
        else:
            name='high card'
        return name

    def tell_hand_ranking(self):
        if self.is_flush()==True:
            if self.is_straight()==None:
                name='flush'
            else:
                name='straight flush'
        elif self.is_straight()!=None:
            name='straight'
        else:
            name=self.find_a_kind()
        return name
    def hand_ranking(self):
        if self.tell_hand_ranking()=='straight flush':
            rank=9
        elif self.tell_hand_ranking()=='four of a kind':
            rank=8
        elif self.tell_hand_ranking()=='full house':
            rank=7            
        elif self.tell_hand_ranking()=='flush':
            rank=6
        elif self.tell_hand_ranking()=='straight':
            rank=5
        elif self.tell_hand_ranking()=='three of a kind':
            rank=4
        elif self.tell_hand_ranking()=='two pair':
            rank=3
        elif self.tell_hand_ranking()=='one pair':
            rank=2
        elif self.tell_hand_ranking()=='high card':
            rank=1
        return rank

    def tuple(self):
        a=[]
        if self.hand_ranking()==2:                                # 원페어인 경우
            for i in self.cards:
                a.append(i[0])
            for z in a:
                if a.count(z)==2:
                    onepair=z
                    break
            for v in range(5):
                if self.cards[v][0]==onepair:
                    b=self.cards.pop(v)
                    self.cards.insert(0,b)
            return (self.hand_ranking(),self.cards)
        elif self.hand_ranking()==3:                              # 투페어인 경우
            for i in self.cards:
                a.append(i[0])
            for z in a:
                if a.count(z)==1:
                    notpair=z
            for v in range(5):
                if self.cards[v][0]==notpair:
                    b=self.cards.pop(v)
                    self.cards.insert(4,b)
            return (self.hand_ranking(),self.cards)
        elif self.hand_ranking()==4:                              # three of a kind인 경우
            for i in self.cards:
                a.append(i[0])
            for z in a:
                if a.count(z)==3:
                    triple=z
                    break
            for v in range(5):
                if self.cards[v][0]==triple:
                    b=self.cards.pop(v)
                    self.cards.insert(0,b)
            return (self.hand_ranking(),self.cards)
        elif self.hand_ranking()==8:                               # four of a kind인 경우
            for i in self.cards:
                a.append(i[0])
            for z in a:
                if a.count(z)==4:
                    notpair=z
                    break
            for v in range(5):
                if self.cards[v][0]==notpair:
                    b=self.cards.pop(v)
                    self.cards.insert(0,b)
            return (self.hand_ranking(),self.cards)            
        else:
            return (self.hand_ranking(),self.cards)

        
    def values(self):
        self.tuple()
        b=dict(zip(Card.ranks, range(2, 2+len(Card.ranks))))
        a=[]
        c=[]
        for i in self.cards:
            a.append(b[i[0]])
        if self.hand_ranking()==2:                # 원페어인 경우 쌍을 제외한 카드에서 랭크가 영어인 경우 다시 재정렬 필요함(ex A와 Q중에 A가 높음)
            for i in range(2):
                c.append(a[i])
            del a[0]
            del a[0]
            a.sort(reverse=True)
            c+=a
            return c
        elif self.hand_ranking()==3:              # 투페어인 경우 쌍 2개의 랭크에 영어가 포함되어 있는 경우 재정렬 필요함
            for i in range(4):
                c.append(a[i])
            c.sort(reverse=True)
            for z in range(4):
                del a[0]
            c+=a
            return c
        elif self.hand_ranking()==8 or self.hand_ranking()==4:       # three of a kind, four of a kind인 경우 재정렬 필요x(트리플 링크 값이 같을 경우는 없음)
            return a
        else:                                     # 나머지 족보들: 랭크가 영어인 카드 때문에 재정렬 필요
            a.sort(reverse=True)
            return a




    def __gt__(self,other):
        a=self.tuple()
        b=other.tuple()
        if a[0]!=b[0]:
            return a>b
        else:
            return self.values()>other.values()

    def __lt__(self,other):
        a=self.tuple()
        b=other.tuple()
        if a[0]!=b[0]:
            return a<b
        else:
            return self.values()<other.values()






    
if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    # your test cases here
    hand1=Hands(['KD', 'QD', '7S', '4S', '3H'])                              # high card
    hand2=Hands(['TS', 'TH', '8S', '7H', 'QC'])                              # one pair                          
    hand3=Hands(['QH', 'QS', '6C', '6S', '2H'])                              # two pair
    hand4=Hands(['QC', 'QS', 'QH', 'AH', 'JS'])                              # three of a kind
    hand5=Hands(['8H', '9S', 'TC', '6S', '7H'])                              # straight
    hand6=Hands(['JD', '9D', '8D', '4D', '3D'])                              # flush
    hand7=Hands(['6S', '6H', '6D', 'KC', 'KH'])                              # full house
    hand8=Hands(['5S', '5H', '5D', '5C', '2D'])                              # four of a kind
    hand9=Hands(['7C', '8C', '9C', 'TC', 'JC'])                              # straight flush

    test(hand1.tell_hand_ranking()=='high card')
    test(hand2.tell_hand_ranking()=='one pair')
    test(hand3.tell_hand_ranking()=='two pair')
    test(hand4.tell_hand_ranking()=='three of a kind')
    test(hand5.tell_hand_ranking()=='straight')
    test(hand6.tell_hand_ranking()=='flush')
    test(hand7.tell_hand_ranking()=='full house')
    test(hand8.tell_hand_ranking()=='four of a kind')
    test(hand9.tell_hand_ranking()=='straight flush')

    test(hand1.hand_ranking()==1)
    test(hand2.hand_ranking()==2)
    test(hand3.hand_ranking()==3)
    test(hand4.hand_ranking()==4)
    test(hand5.hand_ranking()==5)
    test(hand6.hand_ranking()==6)
    test(hand7.hand_ranking()==7)
    test(hand8.hand_ranking()==8)
    test(hand9.hand_ranking()==9)

    # 튜플 test (one pair, two pair, three of kind, four of a kind인 경우 쌍을 앞으로 배치)

    print(hand1.tuple())
    print(hand2.tuple())
    print(hand3.tuple())
    print(hand4.tuple())
    print(hand5.tuple())
    print(hand6.tuple())
    print(hand7.tuple())
    print(hand8.tuple())
    print(hand9.tuple())

    
    test((hand1 < hand2)==True)               # hand ranking이 다를 경우 크기 비교
    test((hand5 < hand3)==False)
    test((hand6 > hand3)==True)
    test((hand1 > hand2)==False)


    hand11=Hands(['TD', '2C', 'TS', 'AH', 'QS'])         # value 함수에서 원페어일떼 쌍을 제외한 값 재정렬 결과
    print(hand11.tuple())
    print(hand11.values())

    hand10=Hands(['AS', 'AC', 'JS', 'JD', '2H'])         # value 함수에서 투페어일때 쌍끼리 재정렬 결과
    print(hand10.tuple())
    print(hand10.values())

    hand19=Hands(['8H', '9S', 'TC', 'JS', '7H'])         # value 함수에서 나머지 족보(원페어,투페어,three of a kind, four of a kind)일때 랭크 재정렬 결과
    print(hand19.tuple())
    print(hand19.values())


    # 원페어끼리 비교
    
    hand12=Hands(['AS', 'TH', '8S', 'AD', '4C']) 
    hand13=Hands(['5S', 'TH', '8S', '5H', '4C'])   
    hand14=Hands(['5D', 'TH', '8S', 'AH', 'TC'])          # hand2=Hands(['TS', 'TH', '8S', '7H', 'QC'])
    test((hand2 < hand12)==True)                          # hand2와 hand12 원페어 쌍 다른 경우 1
    test((hand2 > hand13)==True)                          # hand2와 hand13 원페어 쌍 다른 경우 2
    test((hand2 < hand14)==True)                          # hand2와 hand14 원페어 쌍 같은경우

    # 투페어끼리 비교
    hand15=Hands(['JH', '2S', '6C', 'JS', '2H'])          
    hand16=Hands(['QH', '7S', '7C', '6S', 'QH'])
    hand17=Hands(['QH', 'QS', '6C', '6S', '9H'])          # hand3=Hands(['QH', 'QS', '6C', '6S', '2H'])
    test((hand3 > hand15)==True)                          # hand3와 hand15 두페어 쌍이 모두 다른 경우
    test((hand3 < hand16)==True)                          # hand3와 hand16 두페어 쌍이 하나만 같은 경우
    test((hand3 < hand17)==True)                          # hand3와 hand17 두페어 쌍이 둘다 같은 경우

    # hand_ranking이 같은 경우 비교
    hand20=Hands(['8D', 'QD', 'AS', '2S', '3H'])                # hand1=Hands(['KD', 'QD', '7S', '4S', '3H'])
    test((hand1 < hand20)==True)                                # 둘다 high card
    hand18=Hands(['8H', '9S', 'TC', 'JS', '7H'])                # hand5=Hands(['8H', '9S', 'TC', '6S', '7H']) 
    test((hand5 < hand18)==True)                                # 둘다 straight
    hand21=Hands(['8D', 'TD', 'JD', '4D', '2D'])                # hand6=Hands(['JD', '9D', '8D', '4D', '3D'])
    test((hand6 < hand21)==True)                                # 둘다 flush
    hand22=Hands(['7S', '7H', '7D', 'AC', 'AH'])                # hand7=Hands(['6S', '6H', '6D', 'KC', 'KH'])
    test((hand7 < hand22)==True)                                # 둘다 full house
    hand23=Hands(['2C', '3C', '6C', '4C', '5C'])                # hand9=Hands(['7C', '8C', '9C', 'TC', 'JC']) 
    test((hand9 > hand23)==True)                                # 둘다 straight flush

    # three of a kind끼리 비교
    hand24=Hands(['AC', 'AS', 'AH', '3H', '9S'])                #hand4=Hands(['QC', 'QS', 'QH', 'AH', 'JS'])
    test((hand4 < hand24)==True)                               

    # four of a kind끼리 비교
    hand25=Hands(['8S', '8H', '5D', '8C', '8D'])                 #hand8=Hands(['5S', '5H', '5D', '5C', '2D'])
    test((hand8 < hand25)==True)                                 

    