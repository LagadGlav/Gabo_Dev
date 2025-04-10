function fetchPlayerInfo() {
    const playerId = document.getElementById('playerId').value;
    fetch(`/api-ag/get_player_info?playerId=${playerId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                displayPlayerInfo(data);
            }
        })
        .catch(error => {
            console.error("Erreur lors de la requête :", error);
        });
}