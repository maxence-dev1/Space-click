from PIL import Image

def decouper_image(image_path, largeur, hauteur, dossier_sortie):
    image = Image.open(image_path)
    
    largeur_totale, hauteur_totale = image.size

    nb_morceaux_largeur = largeur_totale // largeur
    nb_morceaux_hauteur = hauteur_totale // hauteur

    for i in range(nb_morceaux_largeur):
        for j in range(nb_morceaux_hauteur):

            x1 = i * largeur
            y1 = j * hauteur

            x2 = x1 + largeur
            y2 = y1 + hauteur

            morceau = image.crop((x1, y1, x2, y2))

            nom_fichier = f"souris_bonus_{i}.png"  
            chemin_sortie = f"{dossier_sortie}/{nom_fichier}"
            morceau.save(chemin_sortie)

image_path = "autre/Free Smoke Fx Pixel 2/bonus.png"
dossier_sortie = "skin"

decouper_image(image_path, 65, 80, dossier_sortie)
