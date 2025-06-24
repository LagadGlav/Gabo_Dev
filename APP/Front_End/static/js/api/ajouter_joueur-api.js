function newPlayer() {
    const playername = document.getElementById('playernom').value;
    fetch('/api-ap/save_player', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ playername: playername })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            console.log("Liste des variables :", data.variables); // Affiche la liste des variables
        })
        .catch(error => {
            alert("Le serveur doit pas être bien là, petite pensée à lui")
            console.error("Erreur lors de l'envoi des données du joueur :", error);
        });

}