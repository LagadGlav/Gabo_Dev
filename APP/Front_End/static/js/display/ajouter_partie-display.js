function openNewGameForm() {
    document.getElementById('newGameForm').classList.remove('hidden');
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

  document.getElementById('table').classList.remove('hidden');

  const tbody = document
    .getElementById('savedTable')
    .getElementsByTagName('tbody')[0];

  if (tbody.querySelector(`tr[data-player-id="${player.joueur_id}"]`)) {
    alert("Déjà dans la partie !");
    return;
  }

  const newRow = tbody.insertRow();
  newRow.dataset.playerId = player.joueur_id;

  // 1) Nom
  const nameCell  = newRow.insertCell(0);
  // 2) Score (on passe à index 1 puisque l'infoCell est supprimée)
  const scoreCell = newRow.insertCell(1);

  nameCell.innerText = `${player.joueur_nom} (${player.elo})`;
  scoreCell.innerHTML =
    `<input type="number" name="playerScore${player.joueur_id}" required>`;
}


function removeLastPlayerFromTable() {
  const tbody = document
    .getElementById('savedTable')
    .getElementsByTagName('tbody')[0];

  const rowCount = tbody.rows.length;
  if (rowCount === 0) {
    console.warn('Aucune ligne à supprimer');
    return;
  }

  // supprime la dernière ligne
  tbody.deleteRow(rowCount - 1);

  if (rowCount === 1) {
      document.getElementById('table').classList.add('hidden');
  }
}