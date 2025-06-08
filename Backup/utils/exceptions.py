class AppError(Exception):
    """Classe de base pour toutes les exceptions de l'application."""
    pass

class DatabaseError(AppError):
    """Exception levée pour des erreurs de base de données."""
    def __init__(self, message="Erreur liée à la base de données"):
        super().__init__(message)

class NetworkError(AppError):
    """Exception levée pour les erreurs de connexion réseau."""
    def __init__(self, message="Erreur réseau détectée"):
        super().__init__(message)

class StartUpError(AppError):
    """Exception levée pour des erreurs de validation d'entrée."""
    def __init__(self, message="Erreur de démarrage de l'application"):
        super().__init__(message)
