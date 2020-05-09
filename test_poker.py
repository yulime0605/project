import pytest
import random
from card import Card, PKCard, Deck
from poker import Hands

def test_PKCard_init():
    card = PKCard('AC')
    assert card.rank == 'A' and card.suit=='C'
    assert card.card == 'AC'

def test_PKCard_init_exception():
    for face in ['10S','BD','TA']:
        with pytest.raises(ValueError):
            PKCard(face)
def test_PKCard_repr():
    assert repr(PKCard('AC')) == 'AC'

@pytest.fixture
def hand1():
    return Hands(['KD', 'QD', '7S', '4S', '3H'])
@pytest.fixture
def hand2():
    return Hands(['TS', 'TH', '8S', '7H', 'QC'])
@pytest.fixture
def hand3():
    return Hands(['QH', 'QS', '6C', '6S', '2H'])
@pytest.fixture
def hand4():
    return Hands(['QC', 'QS', 'QH', 'AH', 'JS'])
@pytest.fixture
def hand5():
    return Hands(['8H', '9S', 'TC', '6S', '7H'])
@pytest.fixture
def hand6():
    return Hands(['JD', '9D', '8D', '4D', '3D'])
@pytest.fixture
def hand7():
    return Hands(['6S', '6H', '6D', 'KC', 'KH'])
@pytest.fixture
def hand8():
    return Hands(['5S', '5H', '5D', '5C', '2D'])
@pytest.fixture
def hand9():
    return Hands(['7C', '8C', '9C', 'TC', 'JC'])

#원페어 끼리 비교하기 위해 생성
@pytest.fixture
def hand12():
    return Hands(['AS', 'TH', '8S', 'AD', '4C'])
@pytest.fixture
def hand13():
    return Hands(['5S', 'TH', '8S', '5H', '4C'])
@pytest.fixture
def hand14():
    return Hands(['5D', 'TH', '8S', 'AH', 'TC'])

#투페어 끼리 비교하기 위해 생성
@pytest.fixture
def hand15():
    return Hands(['JH', '2S', '6C', 'JS', '2H'])
@pytest.fixture
def hand16():
    return Hands(['QH', '7S', '7C', '6S', 'QH'])
@pytest.fixture
def hand17():
    return Hands(['QH', 'QS', '6C', '6S', '9H'])

#three of a kind끼리 비교하기 위해 생성
@pytest.fixture
def hand24():
    return Hands(['AC', 'AS', 'AH', '3H', '9S'])

#four of a kind끼리 비교하기 위해 생성
@pytest.fixture
def hand25():
    return Hands(['8S', '8H', '5D', '8C', '8D'])

#high card끼리 비교하기 위해 생성
@pytest.fixture
def hand20():
    return Hands(['8D', 'QD', 'AS', '2S', '3H'])

#straight끼리 비교하기 위해 생성
@pytest.fixture
def hand18():
    return Hands(['8H', '9S', 'TC', 'JS', '7H'])

#flush끼리 비교하기 위해 생성
@pytest.fixture
def hand21():
    return Hands(['8D', 'TD', 'JD', '4D', '2D'])

#full house끼리 비교하기 위해 생성
@pytest.fixture
def hand22():
    return Hands(['7S', '7H', '7D', 'AC', 'AH'])

#straight flush끼리 비교하기 위해 생성
@pytest.fixture
def hand23():
    return Hands(['2C', '3C', '6C', '4C', '5C'])






# hand_ranking 찾기 
def test_tell_hand_ranking(hand1,hand2,hand3,hand4,hand5,hand6,hand7,hand8,hand9,hand12,hand13,hand14):    
    assert hand1.tell_hand_ranking() == 'high card' 
    assert hand2.tell_hand_ranking() == 'one pair' 
    assert hand3.tell_hand_ranking() == 'two pair'
    assert hand4.tell_hand_ranking() == 'three of a kind'
    assert hand5.tell_hand_ranking() == 'straight'
    assert hand6.tell_hand_ranking() == 'flush'
    assert hand7.tell_hand_ranking() == 'full house'
    assert hand8.tell_hand_ranking() == 'four of a kind'
    assert hand9.tell_hand_ranking() == 'straight flush'
    assert hand12.tell_hand_ranking() == 'one pair'    
    assert hand13.tell_hand_ranking() == 'one pair'
    assert hand14.tell_hand_ranking() == 'one pair'

# 비교하기
def test_comp(hand1,hand2,hand3,hand4,hand5,hand6,hand7,hand8,hand9,hand12,hand13,hand14,hand15,hand16,hand17,hand18,hand20,hand21,hand22,hand23,hand24,hand25):
    # hand_ranking이 다른 경우
    assert hand1 < hand2
    assert hand5 > hand3
    assert hand6 > hand4
    assert hand7 < hand9
    # hand_ranking이 같은경우
    assert hand2 < hand12         # hand2와 hand12 원페어 쌍 다른 경우 1        
    assert hand2 > hand13         # hand2와 hand13 원페어 쌍 다른 경우 2
    assert hand2 < hand14         # hand2와 hand14 원페어 쌍 같은경우
    assert hand3 > hand15         # hand3와 hand15 두페어 쌍이 모두 다른 경우
    assert hand3 < hand16         # hand3와 hand16 두페어 쌍이 하나만 같은 경우
    assert hand3 < hand17         # hand3와 hand17 두페어 쌍이 둘다 같은 경우
    assert hand4 < hand24         # three of a kind끼리 비교
    assert hand8 < hand25         # four of a kind끼리 비교
    assert hand1 < hand20         # high card끼리 비교
    assert hand5 < hand18         # straight끼리 비교 
    assert hand6 < hand21         # flush끼리 비교
    assert hand7 < hand22         # full house끼리 비교
    assert hand9 > hand23         # straight flush끼리 비교

