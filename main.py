import copy
import random
import pygame

pygame.init()
pygame.mixer.init()

random_bg_music = pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

#===== variables ==================

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 650
HEIGHT = 800
GOLD = (193, 161, 31)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
POKER_GREEN = (0,81,44)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
logo_img = pygame.image.load("logo.png")
logo_img = pygame.transform.scale(logo_img, (606, 257.51))
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 40)
font2 = pygame.font.Font('freesansbold.ttf', 30)
font3 = pygame.font.Font('freesansbold.ttf', 20)
font4 = pygame.font.Font('freesansbold.ttf', 25)
score_font = pygame.font.Font('score_font.otf', 40)
records = [0, 0, 0]
active = False
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
active_hand = False #your turn
outcome = 0
add_score = False

busted = pygame.image.load("bust.png")
busted = pygame.transform.scale_by(busted, 1.7)
lost = pygame.image.load("l.png")
lost = pygame.transform.scale_by(lost, 1.7)
won = pygame.image.load("w.png")
won = pygame.transform.scale_by(won, 1.7)
tie = pygame.image.load("tie.png")
tie = pygame.transform.scale_by(tie, 1.7)

results = [busted, won, lost, tie]

#===== functions ================

#returns buttons depending on the state of the game
def setup(act, record, result):

    button_list = []

    if not act:
        deal = pygame.draw.rect(screen, BLACK, (169, 550, 300, 100), 0, 5)
        pygame.draw.rect(screen, RED, (169, 550, 300, 100), 3, 5)
        deal_text = font.render("Deal Hand", True, WHITE)
        screen.blit(deal_text, (217, 580))
        button_list.append(deal)

    else:
        hit = pygame.draw.rect(screen, BLUE, (70, 625, 200, 80), 0, 5)
        pygame.draw.rect(screen, RED, (70, 625, 200, 80), 3, 5)
        hit_text = font.render("Hit Me", True, WHITE)
        screen.blit(hit_text, (105, 645))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, RED, (380, 625, 200, 80), 0, 5)
        pygame.draw.rect(screen, BLUE, (380, 625, 200, 80), 3, 5)
        stand_text = font.render("Stand", True, WHITE)
        screen.blit(stand_text, (420, 645))
        button_list.append(stand)
        history = font2.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, WHITE)
        screen.blit(history, (114, 740))


    #if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:

        screen.blit(results[result - 1], (-58, -68))
        deal = pygame.draw.rect(screen, BLACK, (285, 625, 75, 80), 0, 5)
        pygame.draw.rect(screen, GOLD, (285, 625, 75, 80), 5, 5)
        screen.blit(font4.render("New", True, WHITE), (295, 640))
        screen.blit(font4.render("Deal", True, WHITE), (295, 665))
        button_list.append(deal)
    
    return button_list


def deal_cards(hand, deck):

    card = random.randint(0, len(deck))
    hand.append(deck[card - 1])
    deck.pop(card - 1)
    return hand, deck


def draw_cards(player, dealer, reveal):

    for i in range (len(player)):
        pygame.draw.rect(screen, WHITE, [80 + (60 * i), 360 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, RED), (85 + 60 * i, 535 + 5 * i))
        screen.blit(font.render(player[i], True, RED), (85 + 60 * i, 365 + 5 * i))
        pygame.draw.rect(screen, BLACK, [80 + (60 * i), 360 + (5 * i), 120, 220], 5, 5)

    for i in range (len(dealer)):
        pygame.draw.rect(screen, WHITE, [385 + (60 * i), 60 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:  
            screen.blit(font.render(dealer[i], True, RED), (390 + 60 * i, 65 + 5 * i))
            screen.blit(font.render(dealer[i], True, RED), (390 + 60 * i, 235 + 5 * i))
        #first card, not time to reveal
        else:
            screen.blit(font.render('??', True, RED), (390 + 60 * i, 65 + 5 * i))
            screen.blit(font.render('??', True, RED), (390 + 60 * i, 235 + 5 * i))
        pygame.draw.rect(screen, BLACK, [385 + (60 * i), 60 + (5 * i), 120, 220], 5, 5)

    # player hasnt finished turn -> dealer hides one card


def calculate_score(hand):

    hand_score = 0
    aces_count = hand.count('A')

    for card in hand:

        if card in cards[:8]:
            hand_score += int(card)
        elif card in cards[8:12]:
            hand_score += 10
        else:
            hand_score += 11


    #aces can be 1 or 11, 11 was assumed, if it was too much 1 is used instead
    while hand_score > 21 and aces_count > 0:
        hand_score -= 10
        aces_count -= 1
    
    return hand_score


def get_score_box_color(score):
    if score > 21:
        return RED
    elif score == 21:
        return GOLD
    else:
        return BLACK


def draw_scores(player, dealer):

    player_scorebox_color = get_score_box_color(player)
    dealer_scorebox_color = get_score_box_color(dealer)
    
    pygame.draw.rect(screen, player_scorebox_color, (20, 380, 55, 55), 0, 5)
    pygame.draw.rect(screen, WHITE, (20, 380, 55, 55), 4, 5)
    screen.blit(score_font.render(str(player), True, WHITE), (32, 384))

    if reveal_dealer:
        pygame.draw.rect(screen, dealer_scorebox_color, (325, 80, 55, 55), 0, 5)
        pygame.draw.rect(screen, WHITE, (325, 80, 55, 55), 4, 5)
        screen.blit(score_font.render(str(dealer), True, WHITE), (337, 84))

def endgame(hand_is_active, dscore, pscore, result, totals, add):

    #result map: 1: bust, 2: win, 3: loss, 4: push
    if not hand_is_active and dscore >= 17:
        if pscore > 21:
            result = 1
        elif dscore < pscore <= 21 or dscore > 21:
            result = 2
        elif pscore < dscore <= 21:
            result = 3
        # a tie
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            elif result == 4:
                totals[2] += 1
            add = False #only want to add to totals once per cycle

    return result, totals, add

        
#==== game loop ===============

running = True
while running:

    timer.tick(fps)
    screen.fill(POKER_GREEN)

    if not active:
        screen.blit(logo_img, (27, 125))
    
    #initial deal to player and dealer, only time two cards will be dealt
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    #once game starts and initial is dealt, calculate scores and display cards
    if active:
        pygame.draw.rect(screen, BLACK, (80, 349, 175, 5), 0, 5)
        pygame.draw.rect(screen, BLACK, (385, 49, 175, 5), 0, 5)
        screen.blit(font3.render("Your Hand", True, WHITE), (111, 324))
        screen.blit(font3.render("Dealers Hand", True, WHITE), (400, 25))

        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = setup(active, records, outcome)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                #not active, buttons[0] is deal hand i.e. start game
                if buttons[0].collidepoint(event.pos):
                    active = True #start the game
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    active_hand = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                #else buttons[0] is "hit me"
                if buttons[0].collidepoint(event.pos) and player_score < 21 and active_hand:
                    my_hand, my_deck = deal_cards(my_hand, game_deck)

                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    active_hand = False
                
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        active_hand = True
                        reveal_dealer = False
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        

    if active_hand and player_score >= 21:
        reveal_dealer = True
        active_hand = False

    outcome, records, add_score = endgame(active_hand, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
    


