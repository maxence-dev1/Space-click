import pygame, sys, time



pygame.init()
largeur_ecran = 1200
hauteur_ecran = 800
ecran = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Space jeu")
jeu = True
statut = False
clock = pygame.time.Clock()
def creer_message( font, message, message_rectangle, couleur):
        if font == 'petite':
            font = pygame.font.SysFont('Lato', 25, False)
        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 30, False)
        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 60, True)

        message_surface = font.render(message, True, couleur)
        message_rect = message_surface.get_rect()
        
        message_rect.centerx, message_rect.centery = message_rectangle

        ecran.blit(message_surface, message_rect)

def afficher_bonus(largeur_ecran, hauteur_ecran):
        image = pygame.transform.scale(pygame.image.load('skin\explosion_bonus\logo.png'),(largeur_ecran//13.33,hauteur_ecran//8.88))
        ecran.blit(image,(largeur_ecran//1.1,hauteur_ecran//1.14))

def afficher_bonus_souris(largeur_ecran, hauteur_ecran):
        image = pygame.transform.scale(pygame.image.load('skin\souris\logo2.png'),(largeur_ecran//12,hauteur_ecran//8))
        ecran.blit(image,(largeur_ecran//1.22,hauteur_ecran//1.17))

while jeu:
    events = pygame.event.get()
    for evenement in events:
        if evenement.type == pygame.QUIT:
            jeu = False
            sys.exit()
    afficher_bonus(largeur_ecran, hauteur_ecran)
    afficher_bonus_souris(largeur_ecran, hauteur_ecran)
    pygame.display.flip()



    