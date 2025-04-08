function openNewGameForm() {
    document.getElementById('newGameForm').classList.remove('hidden');
}

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

var list_player_info =[];
function fetchPlayerInfo_2() {
    const playerId = document.getElementById('playerId').value;
    fetch(`/api-ag/get_player_info?playerId=${playerId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {

                alert(data.error);
            } else {
                list_player_info.push(data)
                console.log(list_player_info)
                addPlayerToTable(data);
            }
        })
        .catch(error => {
            console.error("Erreur lors de la requête :", error);
        });
}

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
            console.log("Liste des variables :", data.variables); // Affiche la liste des variables
        })
        .catch(error => {
            console.error("Erreur lors de l'envoi des données du joueur :", error);
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
document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("savedTable").getElementsByTagName("tbody")[0];
    if (!tableBody) {
        throw new Error("Table body not found.");
    }
    document.getElementById("sendTableButton").addEventListener("click", sendTableToServer);
});



function addPlayerToTable(player) {
    const tableBody = document.getElementById('savedTable').getElementsByTagName('tbody')[0];
    const newRow = tableBody.insertRow();

    // Insérer les cellules dans l'ordre correct
    const playerNameCell = newRow.insertCell(0);
    const playerInfoCell = newRow.insertCell(1);
    const scoreCell = newRow.insertCell(2);

    // Remplir les cellules avec les informations du joueur
    playerNameCell.innerText = `${player.joueur_nom} (${player.elo})`;
    const playerInfo = ` - Parties: ${player.nombre_partie}, Score Total: ${player.score_total}, Ratio Score: ${player.ratio_score}, Ratio Rang: ${player.ratio_rang}`;
    playerInfoCell.innerText = playerInfo;
    scoreCell.innerHTML = `<input type="number" name="playerScore${player.joueur_id}" required>`;

    // Effacer le formulaire d'information du joueur
    document.getElementById('playerForm').reset();
}




function sendTableToServer() {
    const tableBody = document.getElementById("savedTable").getElementsByTagName("tbody")[0];
    const rows = [...tableBody.getElementsByTagName("tr")];
    console.log(`Number of rows: ${rows.length}`);
    if (rows.length === 0) {
        throw new Error("No rows found in the table body.");
    }


    const idsRow = [];
    const scoresRow = [];
    const eloRow = [];

    rows.forEach((row, index) => {
        // Match each table row with the corresponding player in list_player_info
        const player = list_player_info[index];

        if (player) {
            const cells = row.getElementsByTagName("td");
            const scoreInput = cells[2].querySelector("input");

            idsRow.push(player.joueur_id);
            eloRow.push(player.elo);
            if (!scoreInput) {
                throw new Error("Score input field is missing for this row.");
            }
            scoresRow.push(scoreInput.value);
        }
    });

    const tableData = [idsRow, scoresRow, eloRow];

    fetch("/api-ag/save_table", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table: tableData })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error("Erreur lors de l'envoi du tableau :", error);
        });
}

