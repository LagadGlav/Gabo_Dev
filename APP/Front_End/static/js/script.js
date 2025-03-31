document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("sendTableButton").addEventListener("click", sendTableToServer);
});

let gameId = 1; // Initial game ID, should be fetched from the backend and incremented

function openNewGameForm() {
    document.getElementById('newGameForm').classList.remove('hidden');
}

function fetchPlayerInfo() {
    const playerId = document.getElementById('playerId').value;
    fetch(`/get_player_info?playerId=${playerId}`)
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

function displayPlayerInfo(player) {
    const playerInfoDiv = document.getElementById('playerInfo');
    playerInfoDiv.innerHTML = `
        <h3>${player.joueur_nom} (ELO: ${player.elo})</h3>
        <p>Nombre de Parties: ${player.nombre_partie}</p>
        <p>Score Total: ${player.score_total}</p>
        <p>Ratio Score: ${player.ratio_score}</p>
        <p>Ratio Rang: ${player.ratio_rang}</p>
    `;
}


function addPlayerToTable(player) {
    const tableBody = document.getElementById('savedTable').getElementsByTagName('tbody')[0];
    const newRow = tableBody.insertRow();
    newRow.insertCell(0).innerText = gameId;
    const playerInfo = `${player.joueur_nom} (ELO: ${player.elo})<br><small>Parties: ${player.nombre_partie}, Score Total: ${player.score_total}, Ratio Score: ${player.ratio_score}, Ratio Rang: ${player.ratio_rang}</small>`;
    newRow.insertCell(1).innerHTML = playerInfo;
    const scoreCell = newRow.insertCell(2);
    scoreCell.innerHTML = `<input type="number" name="playerScore${player.joueur_id}" required>`;

    // Clear player info section
    document.getElementById('playerForm').reset();
}

function addGame(player) {
    const numPlayers = document.getElementById('numPlayers').value;

    const idsRow = [gameId];
    const dataRow = [numPlayers];

    for (let i = 1; i <= numPlayers; i++) {
        const playerId = document.getElementById(`playerId${player.joueur_id[i]}`).value;
        const playerScore = document.getElementById(`playerScore${i}`).value;

        idsRow.push(playerId);
        dataRow.push(playerScore);
    }

    const table = document.getElementById('gameTable').getElementsByTagName('tbody')[0];

    if (table.rows.length > 0) {
        // Si une ligne existe, on l'écrase
        const existingRow = table.rows[0];
        existingRow.cells[0].innerText = idsRow.join(", ");
        existingRow.cells[1].innerText = dataRow.join(", ");
    } else {
        // Si aucune ligne n'existe, on en ajoute une
        const newRow = table.insertRow();
        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        cell1.innerText = idsRow.join(", ");
        cell2.innerText = dataRow.join(", ");
    }
}

function sendTableToServer() {
    const tableBody = document.getElementById("savedTable").getElementsByTagName("tbody")[0];
    const rows = tableBody.getElementsByTagName("tr");
    const tableData = [[], []];

    tableData[0].push(gameId);
    tableData[1].push(rows.length);

    for (const row of rows) {
        const cells = row.getElementsByTagName("td");
        tableData[0].push(cells[1].innerText.split(' ')[0]); // Extract player ID from name (assuming format "Name (ELO)")
        tableData[1].push(cells[2].querySelector('input').value); // Get player score
    }

    fetch("/save_table", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table: tableData })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            gameId++; // Increment game ID after successful submission
        })
        .catch(error => {
            console.error("Erreur lors de l'envoi du tableau :", error);
        });
}
