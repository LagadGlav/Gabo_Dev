from flask import render_template
from . import main_bp

@main_bp.route('/')
def accueil():
    # Affiche la page d'accueil
    return render_template('accueil.html')

@main_bp.route('/ajouter_partie')
def ajouter_partie():
    # Affiche la page de jeu
    return render_template('ajouter_partie.html')

@main_bp.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html')

