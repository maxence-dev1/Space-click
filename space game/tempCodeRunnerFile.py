import pygame, random, sys, math, time


#le joueur se trouve au centre de l'ecran et des vagues d'ennemis arrivent sur lui. Je veux que lorsqu'il clique sur un ennemi il meurt et si jamais un arrive au milieu (donc sur le joueur le jeu est perdu). Comment m'y prendre ? Pour le moment, j'ai créé une classe Jeu ou j'ai créé les methodes : fonction_principale, afficher_joueur. Je compte aussi créé une autre classe nommé Ennemi qui à pour but de crééer un Ennemi et de le faire se déplacer. Je compte utiliser cette classe pour crééer plusieurs ennemis à la foi dans la fonction_principale. 

# liste des capacitées : 
class Jeu:
    def __init__(self, largeur_ecran, hauteur_ecran):
        #initialiser les musiques
        pygame.mixer.init()
        self.musique_debut = pygame.mixer.Sound("musique_debut.wav")
        self.musique_jeu = pygame.mixer.Sound("musique_jeu.ogg")
        self.musique_fin = pygame.mixer.Sound("musique_fin.ogg")
        self.musique_en_cours = False

        self.ennemi = Ennemi
        pygame.init()
        self.ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
        pygame.display.set_caption("Space jeu")
        self.ecran_acceuil = True
        self.jeu_en_cours = False
        self.vague_en_cours = True
        self.jeu_en_pause = False
        self.ecran_fin = False
        self.statut_jeu = "debut"
        self.jeu_infini = True
        self.nb_ennemi = 0
        self.temps_bonus1 = 0
        self.oui = None
        self.comp_temps = 0
        self.souris_pressee = False


        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran

        # Les variables du joueur
        self.joueur_pos_x = largeur_ecran // 2
        self.joueur_pos_y = hauteur_ecran // 2
        self.joueur_corps = 10

        #la liste des ennemis
        self.liste_ennemis = []

        #parametres pour gerer la difficulté
        self.nb_kill = 0
        self.vitesse = 1

        #paramètres pieces
        self.pieces = 0

    def fonction_principale(self):
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            clock = pygame.time.Clock()
            self.vague_en_cours = True
            while self.jeu_infini:
                print(self.souris_pressee)
                if self.statut_jeu == "debut":
                    self.ecran_debut()
                    pygame.display.flip()
                if self.statut_jeu == "jeu":
                    self.ecran.fill((0,0,0))
                    self.gerer_evenements()
                    self.mise_a_jour()
                    pygame.display.flip()
                    clock.tick(60)
                if self.statut_jeu == "fin" : 
                    self.fin_jeu()
                    pygame.display.flip()
               
            pygame.quit()
            sys.exit()

    def demarrer_musique(self, musique_en_cours, prochaine_musique):
        print()
        musique_en_cours.stop()
        prochaine_musique.play(-1)


    def arreter_musique(self):
        pygame.mixer.stop()

    def ecran_debut(self):
        if not self.musique_en_cours:
            self.musique_debut.play(-1)
            self.musique_en_cours = True
        self.nb_kill = 0
        self.liste_ennemis = []
        self.vitesse = 1
        self.ecran_acceuil = True
        self.jeu_en_cours = False
        self.vague_en_cours = True
        self.jeu_en_pause = False
        self.ecran_fin = False
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.jeu_infini = False
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_RETURN:
                    self.demarrer_musique(self.musique_debut, self.musique_jeu)
                    self.statut_jeu = "jeu"
        image = pygame.transform.scale(pygame.image.load('fond.jpg'),(self.largeur_ecran,self.hauteur_ecran))
        self.ecran.blit(image,(0,0)) 
        self.creer_message('grande', "Appuyez sur entrer pour jouer", (self.largeur_ecran//2, self.hauteur_ecran//2+(self.hauteur_ecran)//3), (255, 0, 255))



    def afficher_joueur(self):
        skin_joueur = pygame.transform.scale(pygame.image.load('skin\skin_joueur.png'),(50,50))
        self.ecran.blit(skin_joueur,(self.largeur_ecran//2-20, self.hauteur_ecran//2-20))
    def generer_ennemis(self, nb = 2):
        if len(self.liste_ennemis) <= 100:
            self.nb_ennemi +=1
            for _ in range(nb):
                self.liste_ennemis.append(Ennemi(self, self.vitesse))
        else : 
            self.vitesse += 0.001

    def afficher_ennemis(self):
        for ennemi in self.liste_ennemis:
            if ennemi.vivant:
                ennemi.bouger_ennemi()
                ennemi.afficher_ennemi()
        self.afficher_joueur()


    def gerer_evenements(self):
            gauche, _, _ = pygame.mouse.get_pressed()
            if gauche:
                self.souris_pressee = True
            else:
                self.souris_pressee = False
            events = pygame.event.get()
            for evenement in events:
                if evenement.type == pygame.QUIT:
                    self.jeu_infini = False
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_ESCAPE:
                        self.jeu_en_pause = not self.jeu_en_pause
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_k:
                        self.jeu_infini = False
                    elif evenement.key == pygame.K_b:
                        self.comp_temps = time.time()
                        if self.pieces > 10 and time.time() >= self.temps_bonus1 +10:
                            self.bonus_explosion()
                            
                        else : 
                            if time.time() >= self.comp_temps +1:
                                self.oui = True
                            else : 
                                self.oui = False
                        
                    elif evenement.key == pygame.K_n:
                        if self.pieces > 2 :
                            self.bonus_souris()
                        
            for evenement in events:
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    souris_x, souris_y = pygame.mouse.get_pos()
                    for ennemi in self.liste_ennemis:
                        if ennemi.vivant and ennemi.pos_x - 20 <= souris_x <= ennemi.pos_x + 20 and \
                                ennemi.pos_y - 20 <= souris_y <= ennemi.pos_y + 20:
                            ennemi.vivant = False
                            self.vague_en_cours = True
                            ennemi.explosion_meteor()
                            self.nb_kill +=1
                            self.pieces +=1
            if self.vague_en_cours:
                self.generer_ennemis()
                self.vague_en_cours = False


    def afficher_score(self):
        self.creer_message('moyenne', f"score : {self.nb_kill}", (self.largeur_ecran//2, 30), ((255,0,0)))    
    
    
    def pause(self):
        image = pygame.transform.scale(pygame.image.load('fond.jpg'),(self.largeur_ecran,self.hauteur_ecran))
        self.ecran.blit(image,(0,0))
        
        self.creer_message('grande', "Jeu en pause", (self.largeur_ecran//2, self.hauteur_ecran//2+(self.hauteur_ecran)//3), (255, 0, 255))

        self.afficher_score()

    def mise_a_jour(self):
        if not self.jeu_en_pause:
            self.afficher_joueur()
            self.afficher_score()
            self.afficher_ennemis()
            self.afficher_pieces()
            self.afficher_bonus()
            
        else :
            self.pause()


    def creer_message(self, font, message, message_rectangle, couleur):
        if font == 'petite':
            font = pygame.font.SysFont('Lato', 20, False)
        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 50, False)
        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 60, True)

        message_surface = font.render(message, True, couleur)
        message_rect = message_surface.get_rect()
        
        message_rect.centerx, message_rect.centery = message_rectangle

        self.ecran.blit(message_surface, message_rect)

    def fin_jeu(self):
        pygame.event.pump()
        events = pygame.event.get()
        for evenement in events:
            if evenement.type == pygame.QUIT:  
                self.jeu_infini = False
        image = pygame.transform.scale(pygame.image.load('fond.jpg'),(self.largeur_ecran,self.hauteur_ecran))
        self.ecran.blit(image,(0,0))
        self.creer_message("grande", "Perdu ! ", (self.largeur_ecran//2, self.hauteur_ecran//9), (255,255,255))
        a = self.bouton("Jouer encore", 100, 200, self.largeur_ecran//2, self.hauteur_ecran//3 + self.hauteur_ecran//2, (255,0,255))
        if a == 1 :
            self.statut_jeu = "debut"
            self.musique_en_cours = False
            self.arreter_musique()

    
    def bouton(self, texte, hauteur, largeur, x, y, couleur):
        pygame.draw.rect(self.ecran, couleur, (x - largeur//2,y-hauteur//2,largeur,hauteur))
        self.creer_message("moyenne", texte, (x,y), (255,255,255))
        for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    self.ecran_fin = False
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    souris_x, souris_y = pygame.mouse.get_pos()
                    if x - largeur//2 <= souris_x <= x + largeur//2 and y - hauteur//2 <= souris_y <= y + hauteur//2:
                        return 1
        

    def effet_lumière(self):
        self.ecran.fill((80,80,80))
        pygame.display.flip()
        pygame.time.delay(10)
        self.afficher_score()
        self.ecran.fill((70,70,70))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((60,60,60))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((50,50,50))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((40,40,40))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((30,30,30))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((20,20,20))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((10,10,10))
        pygame.display.flip()
        pygame.time.delay(10)
        self.ecran.fill((0,0,0))
        pygame.display.flip()

    

    def afficher_pieces(self):
        image = pygame.transform.scale(pygame.image.load('skin\piece.png'),(70,70))
        self.ecran.blit(image,(self.largeur_ecran//100,self.hauteur_ecran//70))
        self.creer_message("moyenne", str(self.pieces), (self.largeur_ecran//17,self.hauteur_ecran//21), ((255,255,255)))


    def afficher_bonus(self):
        if self.oui:
            image = pygame.transform.scale(pygame.image.load('skin\explosion_bonus\logo3.png'),(self.largeur_ecran//13.33,self.hauteur_ecran//8.88))
            self.ecran.blit(image,(self.largeur_ecran//1.1,self.hauteur_ecran//1.14))
  
        else:
            if self.pieces < 10 or  time.time() <= self.temps_bonus1 +10:
                image = pygame.transform.scale(pygame.image.load('skin\explosion_bonus\logo2.png'),(self.largeur_ecran//13.33,self.hauteur_ecran//8.88))
                self.ecran.blit(image,(self.largeur_ecran//1.1,self.hauteur_ecran//1.14))

            else :    
                image = pygame.transform.scale(pygame.image.load('skin\explosion_bonus\logo.png'),(self.largeur_ecran//13.33,self.hauteur_ecran//8.88))
                self.ecran.blit(image,(self.largeur_ecran//1.1,self.hauteur_ecran//1.14))


    def bonus_explosion(self):
            self.temps_bonus1 = time.time()
            self.effet_lumière()
            self.pieces = self.pieces - 10
            self.liste_ennemis = []
            for i in range(10):
                self.ecran.fill((0,0,0))
                image = pygame.transform.scale(pygame.image.load(f'skin\explosion_bonus\explosion_bonus_{i}.png'),(self.largeur_ecran,self.hauteur_ecran))
                self.ecran.blit(image,(0,0))
                pygame.display.flip()
                pygame.time.delay(50)
            for ennemi in self.liste_ennemis:
                ennemi.vivant = False
                self.nb_kill +=1
            self.generer_ennemis(self.nb_ennemi)
            

    def bonus_souris(self):
                print('ouiiiiiii')
                souris_x, souris_y = pygame.mouse.get_pos()
                if self.souris_pressee:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    for ennemi in self.liste_ennemis:
                            if ennemi.vivant and ennemi.pos_x - 20 <= souris_x <= ennemi.pos_x + 20 and \
                                    ennemi.pos_y - 20 <= souris_y <= ennemi.pos_y + 20:
                                ennemi.vivant = False
                                self.vague_en_cours = True
                                ennemi.explosion_meteor()
                                self.nb_kill +=1
                                self.pieces +=1
                                print("mort")




#Est sensé créer un ennemi et gérer son apparition, ses déplacements et sa mort.
class Ennemi:
    def __init__(self, jeu, vitesse):
        self.ecran = jeu.ecran
        self.jeu = jeu
        self.vivant = True
        self.corps = 50
        directions = random.choice(['gauche','droite','haut','bas'])

        if directions == 'gauche':
            self.pos_x = -self.corps
            self.pos_y = random.randint(0, self.jeu.hauteur_ecran - self.corps)
        elif directions == 'droite':
            self.pos_x = self.jeu.largeur_ecran
            self.pos_y = random.randint(0, self.jeu.hauteur_ecran - self.corps)
        elif directions == 'haut':
            self.pos_x = random.randint(0, self.jeu.largeur_ecran - self.corps)
            self.pos_y = -self.corps
        elif directions == 'bas':
            self.pos_x = random.randint(0, self.jeu.largeur_ecran - self.corps)
            self.pos_y = self.jeu.hauteur_ecran
        
        self.vitesse = vitesse

        

    def afficher_ennemi(self):
        skin_ennemi = pygame.transform.scale(pygame.image.load('skin\meteor.png'),(self.corps,self.corps))
        self.ecran.blit(skin_ennemi,(self.pos_x - self.corps//2, self.pos_y - self.corps//2))
        
        
        
        
    def bouger_ennemi(self):
        if self.vivant:

            x = self.pos_x
            y = self.pos_y

            dx = x - self.jeu.largeur_ecran // 2
            dy = y - self.jeu.hauteur_ecran // 2
            distance = math.sqrt(dx ** 2 + dy ** 2)

            dx = (dx / distance) * self.vitesse
            dy = (dy / distance) * self.vitesse
            
            if 0 <= distance <= 30:
                jeu.demarrer_musique(jeu.musique_jeu, jeu.musique_fin)
                self.jeu.statut_jeu = "fin"
                

            self.pos_x -= dx
            self.pos_y -= dy

    def explosion_meteor(self,):
            for i in range(1,11) :
                self.ecran.fill((0,0,0))
                skin = pygame.transform.scale(pygame.image.load(f'skin\explosion\explosion{i}.png'),(60,60))
                self.ecran.blit(skin,(self.pos_x-30, self.pos_y-30))
                self.jeu.mise_a_jour()
                self.jeu.gerer_evenements()
                pygame.display.flip()
                pygame.time.delay(10)

   

jeu = Jeu(1000, 800)
jeu.fonction_principale()
