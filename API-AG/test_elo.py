import random
import math
import statistics

# --- Vos fonctions de calcul ELO et d'agrégation ---

def calculate_elo(current_elo, opponent_elo, score_diff, result, k=1):
    """
    Calcule la variation d'Elo à partir des paramètres.

    Args:
        current_elo (int): Elo actuel du joueur.
        opponent_elo (int): Elo de l'adversaire.
        score_diff (int): Différence de score (valeur absolue).
        result (float): Résultat du jeu (1 pour victoire, 0 pour défaite, 0.5 pour match nul).
        k (int): Facteur d'ajustement (par défaut 1).

    Returns:
        float: Variation Elo calculée.
    """
    # Calcul du résultat attendu à partir de la formule Elo classique
    expected_result = 1 / (1 + 10 ** ((opponent_elo - current_elo) / 400))

    # Lorsque la différence de score est nulle, on considère match nul
    if score_diff == 0:
        result = 0.5
        return k * (result - expected_result) * score_diff

    # Variation Elo = facteur k * différence de score * (résultat obtenu - résultat attendu)
    var_elo = k * score_diff * (result - expected_result)
    return var_elo


def get_var_elo(table):
    """
    Calcule les variations Elo pour chaque joueur en comparant par paire.

    La table est une liste à trois éléments :
      - table[0] : liste des IDs des joueurs,
      - table[1] : liste des scores,
      - table[2] : liste des valeurs Elo.

    Pour chaque paire (i,j), le joueur i est supposé gagner (result = 1) et j perdre (result = 0).

    Returns:
        list: Liste contenant la variation totale d'Elo pour chaque joueur.
    """
    elo = table[2]
    var_elo = [0] * len(elo)  # Initialisation à zéro pour chaque joueur

    for i in range(len(elo) - 1):
        for j in range(i + 1, len(elo)):
            # On récupère les ELO de la paire et la différence absolue des scores
            current_elo = elo[i]
            opponent_elo = elo[j]
            score_diff = abs(table[1][i] - table[1][j])

            # Considérons que le joueur i obtient une victoire (result = 1) et j une défaite (result = 0)
            var_elo[i] += calculate_elo(current_elo, opponent_elo, score_diff, 1)
            var_elo[j] += calculate_elo(opponent_elo, current_elo, score_diff, 0)

    return var_elo


def sort_table(table):
    """
    Trie la table (liste de trois listes : IDs, scores, Elo) selon l'ordre croissant des scores
    en utilisant un tri par insertion.

    Args:
        table (list): Table contenant les IDs, scores et abscisses Elo.

    Returns:
        list: Table triée.
    """
    n = len(table[1])
    table[1] = [int(score) for score in table[1]]  # S'assurer que les scores sont des entiers
    try:
        for i in range(1, n):
            key = table[1][i]
            key_id = table[0][i]
            key_elo = table[2][i]
            j = i - 1
            # Le tri par insertion (ici tri croissant, c'est-à-dire que le score le plus bas est en tête)
            while j >= 0 and table[1][j] > key:
                table[1][j + 1] = table[1][j]
                table[0][j + 1] = table[0][j]
                table[2][j + 1] = table[2][j]
                j -= 1
            table[1][j + 1] = key
            table[0][j + 1] = key_id
            table[2][j + 1] = key_elo
        return table
    except Exception as e:
        raise Exception(f"Error sorting table : {e}")


# --- Simulation de l'insertion via une file de traitement ---

class Game:
    """
    Objet représentant une session de jeu.
    """
    def __init__(self, game_id, nb_joueurs, id_joueur, score, rang, var_elo):
        self.game_id = game_id
        self.nb_joueurs = nb_joueurs
        self.id_joueur = id_joueur
        self.score = score
        self.rang = rang
        self.var_elo = var_elo

    def __repr__(self):
        return (f"Game(game_id={self.game_id}, id_joueur={self.id_joueur}, "
                f"score={self.score}, rang={self.rang}, var_elo={self.var_elo})")


class DummyQueue:
    """
    Petite file simplifiée pour stocker les objets Game.
    """
    def __init__(self):
        self.items = []

    def add_queue(self, item):
        self.items.append(item)

    def empty_queue(self):
        items = self.items[:]
        self.items.clear()
        return items

    def __repr__(self):
        return repr(self.items)


# Variables globales pour la simulation
Q = DummyQueue()
# Dans un environnement multi-threadé, vous utiliseriez threading.Lock(). Ici, pour la simulation, on ne fait rien.
lock = None
game_id = 0  # ID global des parties

def insertion(table):
    """
    Simule l'insertion des données de match dans une file de traitement.
    Pour chaque joueur de la table triée, le rang est défini par la position (i+1),
    et la variation Elo est ajustée par math.floor(var_elo[i] / 10).

    Args:
        table (list): Table triée contenant les IDs, scores et ELO.

    Returns:
        bool: True si l'insertion s'est déroulée correctement.
    """
    global game_id
    var_elo_list = get_var_elo(table)

    for i in range(len(table[0])):
        id_joueur = table[0][i]
        score = table[1][i]
        nb_joueurs = len(table[0])
        rang = i + 1
        # Ajustement de la variation (division par 10, puis arrondi par défaut)
        var_elo_adjusted = math.floor(var_elo_list[i] / 10)

        # Création de l'objet Game
        game = Game(game_id, nb_joueurs, id_joueur, score, rang, var_elo_adjusted)
        Q.add_queue(game)  # Insertion dans la file (ici sans lock effectif)

    return True


# --- Jeu de Test Complet ---

def test_full_flow(num_players):
    """
    Crée un jeu de test avec 'num_players' joueurs ayant des scores et ELO variés.
    On simule l'ensemble du processus :
      - Génération de la table initiale,
      - Tri de la table selon les scores,
      - Calcul des variations Elo via les confrontations par paires,
      - Simulation de l'insertion (création d'objets Game et ajout dans la file).

    Affiche ensuite les données initiales, la table triée, les variations Elo et les nouveaux
    ELO simulés pour observer l'impact et la dispersion.
    """
    random.seed(15558)
    # Générer aléatoirement les données pour chaque joueur :
    player_ids = list(range(1, num_players + 1))
    # Scores entre 0 et 200
    scores = [random.randint(0, 116) for _ in range(num_players)]
    # Elo entre 100 et 2500 pour simuler d'importants écarts
    elos = [random.randint(450, 1500) for _ in range(num_players)]
    table = [player_ids, scores, elos]

    # Tri de la table par score (ordre croissant)
    sorted_table = sort_table(table)
    print("\n=== Table Triée (Score croissant) ===")
    print("IDs :", sorted_table[0])
    print("Scores :", sorted_table[1])
    print("ELOs :", sorted_table[2])

    # Calcul des variations Elo pour la table triée
    var_elo = get_var_elo(sorted_table)
    print("\n=== Variations Elo Par Joueur ===")
    for i, v in enumerate(var_elo):
        print(f"Joueur {sorted_table[0][i]} : Variation Elo = {int(v/10)} ({sorted_table[1][i]} {sorted_table[2][i]})")

    # Calcul des nouveaux Elo (ajustement en divisant par 10, arrondi avec floor)
    new_elos = [elo + math.floor(v / 10) for elo, v in zip(sorted_table[2], var_elo)]
    print("\n=== Nouvelles Valeurs Elo Simulées ===")
    print(new_elos)

    # Quelques statistiques sur les variations et nouveaux Elo
    print("\n=== Statistiques sur les Variations Elo ===")
    print("Variation min :", min(var_elo)*0.1)
    print("Variation max :", max(var_elo)*0.1)
    print("Variation moyenne :", statistics.mean(var_elo))

    print("\n=== Statistiques sur les Nouveaux ELO ===")
    print("ELO min :", min(new_elos))
    print("ELO max :", max(new_elos))
    print("ELO moyen :", statistics.mean(new_elos))


if __name__ == "__main__":
    test_full_flow(7)
