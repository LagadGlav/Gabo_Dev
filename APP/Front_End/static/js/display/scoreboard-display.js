document.addEventListener('DOMContentLoaded', function() {
    const playerInput = document.getElementById('playerId');

    playerInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            fetchPlayerInfo();
        }
    });
});

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

    let ranking = 0;
    players.forEach(player => {
        ranking++;

        // Create a new card for each player
        const playerCard = document.createElement('div');
        playerCard.classList.add('player-card');

        // Default styling values
        let trophy = "";
        let backgroundColor = "linear-gradient(135deg, #007bff, #0056b3)"; // Default blue
        let cardScale = 1; // Default scale

        // Customization for the top 3 players using Bootstrap-inspired colors with vendor prefixes
        if (ranking === 1) {
            trophy = "🏆"; // Gold trophy
            cardScale = 1.08;
            // Fallback color
            playerCard.style.backgroundColor = "#ffc107";
            // Vendor-prefixed gradient
            playerCard.style.backgroundImage = "-webkit-linear-gradient(135deg, #ffc107, #ffca2c)";
            // Standard gradient
            playerCard.style.backgroundImage = "linear-gradient(135deg, #ffc107, #ffca2c)";
        } else if (ranking === 2) {
            trophy = "🥈"; // Silver trophy
            cardScale = 1.04;
            playerCard.style.backgroundColor = "#adb5bd";
            playerCard.style.backgroundImage = "-webkit-linear-gradient(135deg, #adb5bd, #ced4da)";
            playerCard.style.backgroundImage = "linear-gradient(135deg, #adb5bd, #ced4da)";
        } else if (ranking === 3) {
            trophy = "🥉"; // Bronze trophy
            cardScale = 1.02;
            playerCard.style.backgroundColor = "#fd7e14";
            playerCard.style.backgroundImage = "-webkit-linear-gradient(135deg, #fd7e14, #e8590c)";
            playerCard.style.backgroundImage = "linear-gradient(135deg, #fd7e14, #e8590c)";
        }

        if ([1, 2, 3].includes(ranking)) {
            // Generate the card content
            playerCard.innerHTML = `
            <h4 style="cursor: pointer;">${trophy} ${player.joueur_nom} (${player.elo})</h4>
            <div class="player-details hidden">
                <p>Number of Games: ${player.nombre_partie}</p>
                <p>Total Score: ${player.score_total}</p>
                <p>Score Ratio: ${player.ratio_score}</p>
                <p>Rank Ratio: ${player.ratio_rang}</p>
            </div>
        `;
        } else {
            // Generate the card content
            playerCard.innerHTML = `
                <h4 style="cursor: pointer;">${ranking} ${player.joueur_nom} (${player.elo})</h4>
                <div class="player-details hidden">
                    <p>Number of Games: ${player.nombre_partie}</p>
                    <p>Total Score: ${player.score_total}</p>
                    <p>Score Ratio: ${player.ratio_score}</p>
                    <p>Rank Ratio: ${player.ratio_rang}</p>
                </div>
            `;
        }

        // Append the new card to the scoreboard container
        scoreboardContainer.appendChild(playerCard);

        // Make the entire card clickable to toggle the details
        playerCard.addEventListener('click', () => {
            const details = playerCard.querySelector('.player-details');
            details.classList.toggle('hidden');
        });
    });
}

// On page load
document.addEventListener('DOMContentLoaded', () => {
    fetchAllPlayers();
});

// When the DOM is ready, attach event listeners to the toggle buttons.
document.addEventListener('DOMContentLoaded', function() {
    const toggleIDBtn = document.getElementById('toggleID');
    const toggleNameBtn = document.getElementById('toggleName');
    // Toggle the entire scoreboard container
    toggleIDBtn.addEventListener('click', function() {
        if (!toggleIDBtn.classList.contains('active')) {
            toggleIDBtn.classList.add('active');
            toggleNameBtn.classList.remove('active');
        }
    });
    toggleNameBtn.addEventListener('click', function() {
        if (!toggleNameBtn.classList.contains('active')) {
            toggleNameBtn.classList.add('active');
            toggleIDBtn.classList.remove('active');
        }
    });
});


