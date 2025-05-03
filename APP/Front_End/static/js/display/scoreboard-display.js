function displayPlayerInfo(player) {
    // Get the container for player cards.
    const playerInfoContainer = document.getElementById('playerInfoContainer');

    // Create a new card element.
    const newCard = document.createElement('div');
    newCard.classList.add('card');

    // Set the HTML content of the new card.
    newCard.innerHTML = `
        <button class="close-btn" onclick="closeCard(this)">&times;</button>
        <h3>${player.joueur_nom} (${player.elo})</h3>
        <p>Number of Games: ${player.nombre_partie}</p>
        <p>Total Score: ${player.score_total}</p>
        <p>Score Ratio: ${player.ratio_score}</p>
        <p>Rank Ratio: ${player.ratio_rang}</p>
    `;

    // Append the new card to the container.
    playerInfoContainer.appendChild(newCard);
}

function closeCard(button) {
    // Remove the card that contains the clicked button.
    button.parentElement.remove();
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('find_player').addEventListener('click', function() {
        const element = document.getElementById('playerInfo');
        if (element) {
            if (element.classList.contains('hidden')) {
                element.classList.remove('hidden');
            }
        } else {
            console.error("Erreur ID !");
        }
    });
});

// Display players in the scoreboard container (with id "scrollable")
function displayPlayers(players) {
    const scoreboardContainer = document.getElementById('scrollable');
    // Clear any previous content
    scoreboardContainer.innerHTML = '';

    players.forEach(player => {
        // Create a new card for each player
        const playerCard = document.createElement('div');
        playerCard.classList.add('player-card');
        playerCard.innerHTML = `
            <h4>${player.joueur_nom} (${player.elo})</h4>
            <p>Score Ratio: ${player.ratio_score} Rank Ratio: ${player.ratio_rang}</p>
            <p>Number of Games: ${player.nombre_partie}</p>
        `;
        // Append it to the scoreboard container
        scoreboardContainer.appendChild(playerCard);
    });
}

// When you want to refresh the list (for example, on page load):
document.addEventListener('DOMContentLoaded', () => {
    fetchAllPlayers();
});