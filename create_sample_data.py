"""
Script pour créer un fichier Excel de test basé sur :
le mythique groupe de métal français Desybes que des dizaines de milliers de fans
attendent avec impatience au non mois mythique Hellfest.
"""
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import random


def create_sample_excel():
    """
    Créer un fichier Excel d'exemple avec plusieurs feuilles.
    """
    # Feuille 1 : Groupe
    groupe_data = {
        'ID': [1],
        'Nom': ['Desybes'],
        'Genre': ['Metal'],
        'Web': ['www.desybes.com'],
        'YouTube': ['youtube.com/@desybes'],
        'Année Formation': [2004]
    }
    df_groupe = pd.DataFrame(groupe_data)
    
    # Feuille 2 : Membres
    membres_data = {
        'ID Membre': [1, 2, 3, 4],
        'ID Groupe': [1, 1, 1, 1],
        'Prénom': ['Sylvain', 'Benoît', 'Silvère', 'Julien'],
        'Nom': ['Oriat', 'Quelet', 'Oriat', 'Mativet'],
        'Poste': ['Guitariste', 'Guitariste/Chanteur', 'Bassiste', 'Batteur'],
        'Actif': [True, True, True, True]
    }
    df_membres = pd.DataFrame(membres_data)
    
    # Feuille 3 : Albums
    albums_data = {
        'ID Album': [1, 2, 3, 4, 5],
        'ID Groupe': [1, 1, 1, 1, 1],
        'Titre': ['Desybes', 'RN 6-32-4', 'L.I.S.', 'Sermon d\'Hypocrite', 'Cieux Connectés'],
        'Année': [2004, 2007, 2012, 2018, 2024],
        'Nombre Pistes': [3, 4, 8, 11, 10],
        'Type': ['Demo', 'EP', 'Album', 'Album', 'Album'],
        'Date Sortie': [
            datetime(2004, 1, 1),
            datetime(2007, 1, 1),
            datetime(2012, 1, 1),
            datetime(2018, 1, 1),
            datetime(2024, 10, 1)
        ]
    }
    df_albums = pd.DataFrame(albums_data)
    
    # Feuille 4 : Concerts et Statistiques
    # Générer 1000 lignes de données aléatoires
    concerts_divers = []
    villes = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Nantes', 'Strasbourg', 
              'Lille', 'Rennes', 'Grenoble', 'Montpellier', 'Nice', 'Clisson', 'Carhaix']
    salles = ['Zenith', 'Bataclan', 'Olympia', 'Hellfest', 'Download Festival', 'Bar Local',
              'Stade de France', 'AccorHotels Arena', 'La Cigale', 'Elysée Montmartre']
    ambiances = ['Electrique', 'Explosive', 'Intense', 'Mythique', 'Légendaire', 'Epic', 
                 'Puissante', 'Mémorable', 'Incroyable', 'Démentielle']
    
    base_date = datetime(2010, 1, 1)
    
    for i in range(1000):
        concert_date = base_date + timedelta(days=random.randint(0, 5475))  # ~15 ans
        concerts_divers.append({
            'ID Concert': i + 1,
            'Ville': random.choice(villes),
            'Salle/Festival': random.choice(salles),
            'Date': concert_date,
            'Spectateurs': random.randint(50, 80000),
            'Ambiance': random.choice(ambiances)
        })
    
    df_concerts = pd.DataFrame(concerts_divers)
    
    # Créer le répertoire data s'il n'existe pas
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Créer le fichier Excel dans le répertoire data
    output_file = data_dir / 'sample_data.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_groupe.to_excel(writer, sheet_name='Groupes', index=False)
        df_membres.to_excel(writer, sheet_name='Membres', index=False)
        df_albums.to_excel(writer, sheet_name='Albums', index=False)
        df_concerts.to_excel(writer, sheet_name='Concerts', index=False)
    
    print(f"✅ Fichier {output_file} créé avec succès !")
    print(f"   - Feuille 'Groupes': {len(df_groupe)} ligne(s)")
    print(f"   - Feuille 'Membres': {len(df_membres)} lignes")
    print(f"   - Feuille 'Albums': {len(df_albums)} lignes")
    print(f"   - Feuille 'Concerts': {len(df_concerts)} lignes")


if __name__ == '__main__':
    create_sample_excel()
