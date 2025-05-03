function openNewGameForm() {
    document.getElementById('newGameForm').classList.remove('hidden');
    document.getElementById('table').classList.remove('hidden');
    document.getElementById('new_game').classList.add('hidden');
}

function resetGameForm() {
    document.getElementById('table').classList.add('hidden');
    document.getElementById('newGameForm').classList.add('hidden');
    document.getElementById('new_game').classList.remove('hidden');
    const tableBody = document.getElementById('savedTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ""; //
    // Réinitialise la liste des joueurs ajoutés
    list_player_info = [];
}

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
}