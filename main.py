import copy
import random
import pygame

pygame.init()

cards = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)

WIDTH = 650
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 40)
font2 = pygame.font.Font('freesansbold.ttf', 30)
active = False

#running total score (wins, losses, ties)
record = [0, 0, 0]

player_score = 0
dealer_score = 0
initial_deal = True
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False


def deal_cards(hand, deck):

    card = random.randint(0, len(deck))
    hand.append(deck[card - 1])
    deck.pop(card - 1)
    print(hand, deck)
    return hand, deck

#draw cards visually
def draw_cards(player, dealer, reveal):
    for i in range (len(player)):
        pygame.draw.rect(screen, 'white', (70 + 70 * i, 460 + (5 * i), 120, 220), 0, 5)
        pygame.draw.rect(screen, 'black', (70 + 70 * i, 460 + (5 * i), 120, 220), 5, 5)

#return buttons, input the state of the game (active hand)
#no act: deal the hand
def setup_game(act, record):

    button_list = []

    if not act:
        
        deal = pygame.draw.rect(screen, 'black', (167, 50, 300, 100), 0, 5)
        pygame.draw.rect(screen, 'red', (167, 50, 300, 100), 3, 5)
        deal_text = font.render("Deal Hand", True, 'white')
        screen.blit(deal_text, (215, 80))
        button_list.append(deal)

    else:

        hit = pygame.draw.rect(screen, 'blue', (50, 625, 200, 80), 0, 5)
        pygame.draw.rect(screen, 'red', (50, 625, 200, 80), 3, 5)
        hit_text = font.render("Hit Me", True, 'white')
        screen.blit(hit_text, (85, 645))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'purple', (400, 625, 200, 80), 0, 5)
        pygame.draw.rect(screen, 'red', (400, 625, 200, 80), 3, 5)
        stand_text = font.render("Stand", True, 'white')
        screen.blit(stand_text, (440, 645))
        button_list.append(stand)
        history = font2.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'black')
        screen.blit(history, (114, 740))
    
    return button_list




running = True
while running:

    timer.tick(fps)
    screen.fill('green')

    #initial deal to player and dealer, only time two cards will be dealt
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        print(my_hand, dealer_hand)
        initial_deal = False

    #once game starts and initial is dealt, calculate scores and display cards
    if active:
        draw_cards(my_hand, dealer_hand, reveal_dealer)

    buttons = setup_game(active, record)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True #start the game
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    outcome = 0

    pygame.display.flip()
    


