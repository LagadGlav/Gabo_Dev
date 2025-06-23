let indexById = {};
let indexByName = {};

document.addEventListener('DOMContentLoaded', function() {
    const playerInput = document.getElementById('playerId');

    playerInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            fetchPlayerInfo();
        }
    });
});

function displayPlayerInfo() {
    // Get the player's search input value
    const playerInput = document.getElementById('playerId').value.trim();

    // Get the toggle buttons
    const toggleIDBtn = document.getElementById('toggleID');
    const toggleNameBtn = document.getElementById('toggleName');


    let player;

    // Determine whether to search by ID or name
    if (toggleIDBtn.classList.contains('active')) {
        id = playerInput
        player = indexById[playerInput]; // Using playerInput as key
    } else if (toggleNameBtn.classList.contains('active')) {
        player = indexByName[playerInput];
    } else {
        alert("Please select either ID or Name to search for the player.");
        return;
    }

    // Ensure the player exists before displaying
    if (!player) {
        alert("Player not found, please try again.");
        return;
    }

    // Create a new card element.
    const newCard = document.createElement('div');
    newCard.classList.add('card');

    // Set the HTML content of the new card.
    newCard.innerHTML = `
        <button class="close-btn" onclick="closeCard(this)">&times;</button>
        <h3>${player.joueur_nom} (${player.elo})</h3>
        <p class="stat-line">
          <span class="stat-label">Number of games played</span>
          <span class="stat-value-player">${Math.round(player.nombre_partie)}</span>
        </p>
        <p class="stat-line">
          <span class="stat-label">Score total</span>
          <span class="stat-value-player">${Math.round(player.score_total)}</span>
        </p>
        <p class="stat-line">
          <span class="stat-label">Average score per game</span>
          <span class="stat-value-player">${Math.round(player.ratio_score)}</span>
        </p>
        <p>Better ${Math.round((1-player.ratio_rang)*100)}% of players in game
        </p>
    `;


    // Création of bouton "Last Games"
    const lastGamesBtn = document.createElement('button');
    lastGamesBtn.classList.add('last-games-btn-player');
    lastGamesBtn.textContent = "Historic";
    lastGamesBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Empêche le déclenchement d'autres événements (comme le toggle)
        window.location.href = `/player/${player.joueur_id}/last-games`;
    });

    // Add a button after innerHTML
    newCard.appendChild(lastGamesBtn);
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
            // Create a player card element for each player
            const playerCard = document.createElement('div');
            playerCard.classList.add('player-card'); // For CSS styling if needed

            // Generate indices for players by name and by ID
            indexByName[player.joueur_nom] = player;
            indexById[player.joueur_id] = player;
            ranking++;

            // Default styling values
            let trophy = "";
            let cardScale = 1;

            // Customization for the top 3 players using gradient backgrounds
            if (ranking === 1) {
                trophy = "🏆"; // Gold trophy
                cardScale = 1.08;
                playerCard.style.backgroundColor = "#ffc107";
                playerCard.style.backgroundImage = "-webkit-linear-gradient(135deg, #ffc107, #ffca2c)";
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

            // Generate the card content along with details that are initially hidden
            // Note: The last games button will be appended inside the details container
    if ([1, 2, 3].includes(ranking)) {
        playerCard.innerHTML = `
            <h4 style="cursor: pointer;">${trophy} ${player.joueur_nom} (${player.elo})</h4>
            <div class="player-details hidden">
                <p class="stat-line">
                  <span class="stat-label">Number of games played</span>
                  <span class="stat-value-player">${Math.round(player.nombre_partie)}</span>
                </p>
                <p class="stat-line">
                  <span class="stat-label">Score total</span>
                  <span class="stat-value-player">${Math.round(player.score_total)}</span>
                </p>
                <p class="stat-line">
                  <span class="stat-label">Average score per game</span>
                  <span class="stat-value-player">${Math.round(player.ratio_score)}</span>
                </p>
           <p>Better ${Math.round((1-player.ratio_rang)*100)}% of players in game</p>
            </div>
        `;
    } else {
        playerCard.innerHTML = `
            <h4 style="cursor: pointer;">${ranking} ${player.joueur_nom} (${player.elo})</h4>
            <div class="player-details hidden">
                <p class="stat-line">
                  <span class="stat-label">Number of games played</span>
                  <span class="stat-value">${Math.round(player.nombre_partie)}</span>
                </p>
                <p class="stat-line">
                  <span class="stat-label">Score total</span>
                  <span class="stat-value">${Math.round(player.score_total)}</span>
                </p>
                <p class="stat-line">
                  <span class="stat-label">Average score per game</span>
                  <span class="stat-value">${Math.round(player.ratio_score)}</span>
                </p>
           <p>Better ${Math.round((1-player.ratio_rang)*100)}% of players in game</p>
            </div>
        `;
    }

        // Grab the details container from the player card
        const detailsContainer = playerCard.querySelector('.player-details');

        // Create the "Last Games" button and append it into the details container
        const lastGamesBtn = document.createElement('button');
        lastGamesBtn.classList.add('last-games-btn-scoreboard');
        lastGamesBtn.textContent = "Historic";
        lastGamesBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent toggling the details when clicking the button
            window.location.href = `/player/${player.joueur_id}/last-games`;
        });
        // Append the button inside the details container so it is hidden when collapsed
        detailsContainer.appendChild(lastGamesBtn);

        // Append the card to the scoreboard container
        scoreboardContainer.appendChild(playerCard);

        // Make the entire card clickable to toggle the details container visibility
        playerCard.addEventListener('click', () => {
            detailsContainer.classList.toggle('hidden');
        });
    });
    console.log(indexById);
    console.log(indexByName);
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


