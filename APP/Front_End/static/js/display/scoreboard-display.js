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

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('find_player').addEventListener('click', function() {
        const element = document.getElementById('playerInfo');
        if (element) {
            if (element.classList.contains('hidden')) {
                element.classList.remove('hidden');
            }
        } else {
            console.error("Élément avec l'ID 'contenu' introuvable !");
        }
    });
});