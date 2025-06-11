function newPlayer() {
    const playerId = document.getElementById('playerId').value;
    const playername = document.getElementById('playernom').value;
    fetch('/api-ap/save_player', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ playerId: playerId, playername: playername })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            console.log("Liste des variables :", data.variables);
        })
        .catch(error => {
            alert("Probably id already taken, please chose an other one")
            console.error("Error sending the player :", error);
        });

}