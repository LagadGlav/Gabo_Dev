document.addEventListener("DOMContentLoaded", async () => {
  // Create and insert a title element above the games container.
  // Assume that "playerName" is a global variable injected into your template.
  const title = document.createElement("h1");
  title.textContent = `Last 10 Games`;
  title.style.textAlign = "center";
  title.style.color = "#fff";
  title.style.margin = "20px 0";

  // Get the container for the cards.
  const gamesContainer = document.getElementById("gamesContainer");
  // Insert the title above the games container.
  gamesContainer.insertAdjacentElement("beforebegin", title);

  // When the DOM is loaded, fetch the game data using your API call.
  const gamesData = await fetchLastTenGames(playerId);
  renderGroupedGameCards(gamesData);
});

/**
 * Renders an expandable card per game group.
 * Collapsed view shows the game date and a summary of the top three players with trophy icons.
 * When expanded, each player's full details are displayed with the score emphasized on the right.
 */
function renderGroupedGameCards(gamesData) {
  const scoreboardContainer = document.getElementById("gamesContainer");
  scoreboardContainer.innerHTML = ""; // Clear previous content

  // Iterate over each game ID in the gamesData object.
  for (const gameId in gamesData) {
    const gameRecords = gamesData[gameId];
    if (!gameRecords || gameRecords.length === 0) continue; // Skip empty groups

    // Sort the game records by rank (ascending; 1 is highest).
    gameRecords.sort((a, b) => a.rang - b.rang);

    // Create the container (card) for this game group.
    const gameCard = document.createElement("div");
    gameCard.classList.add("game-group-card");

    // Create the header section.
    const header = document.createElement("div");
    header.classList.add("game-card-header");

    // Convert the date (from the first record) into a readable format.
    const gameDate = gameRecords[0].date_partie
      ? new Date(gameRecords[0].date_partie).toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric"
        })
      : "N/A";

    // Header displays the game date.
    header.innerHTML = `<h3>${gameDate}</h3>`;

    // Create a toggle button for expand/collapse.
    const toggleBtn = document.createElement("button");
    toggleBtn.classList.add("toggle-btn");
    toggleBtn.textContent = "Expand";
    header.appendChild(toggleBtn);
    gameCard.appendChild(header);

    // --- Collapsed Summary Section ---
    // Show only the top three players in summary (sorted by rank).
    const summaryContainer = document.createElement("div");
    summaryContainer.classList.add("game-summary");
    gameRecords.slice(0, 3).forEach((record) => {
      const summaryItem = document.createElement("p");
      // Determine trophy icon based on player's rank.
      let trophy = "";
      if (record.rang === 1) trophy = "🏆 ";
      else if (record.rang === 2) trophy = "🥈 ";
      else if (record.rang === 3) trophy = "🥉 ";

      summaryItem.innerHTML = `<strong>${trophy}${record.joueur_nom || 'N/A'}</strong>`;
      summaryContainer.appendChild(summaryItem);
    });
    gameCard.appendChild(summaryContainer);

    // --- Expanded Details Section ---
    // This section is hidden by default.
    const detailsContainer = document.createElement("div");
    detailsContainer.classList.add("game-details");
    detailsContainer.style.display = "none";

    // For each record, create a detail item (ordered by rank).
    gameRecords.forEach((record) => {
      const detailItem = document.createElement("div");
      detailItem.classList.add("detail-item");

      // Build a flex container: left part for details; right part shows the score in bigger font.
      detailItem.innerHTML = `
        <div class="detail-left">
          <p style="font-size: 2em;"> ${record.joueur_nom || 'N/A'}</p>
          <p>${record.elo || 'N/A'} (${typeof record.var_elo !== "undefined"
            ? (record.var_elo >= 0 ? '+' : '') + record.var_elo
            : 'N/A'})</p>
        </div>

        <div class="detail-right">
          <p class="big-score">${record.joueur_score || 'N/A'}</p>
        </div>
      `;
      detailsContainer.appendChild(detailItem);
    });
    gameCard.appendChild(detailsContainer);

    // Toggle functionality.
    toggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (detailsContainer.style.display === "none") {
        detailsContainer.style.display = "block";
        toggleBtn.textContent = "Collapse";
      } else {
        detailsContainer.style.display = "none";
        toggleBtn.textContent = "Expand";
      }
    });
    // Optionally, clicking the header toggles expansion.
    header.addEventListener("click", () => {
      if (detailsContainer.style.display === "none") {
        detailsContainer.style.display = "block";
        toggleBtn.textContent = "Collapse";
      } else {
        detailsContainer.style.display = "none";
        toggleBtn.textContent = "Expand";
      }
    });

    // Append the complete game card to the main container.
    scoreboardContainer.appendChild(gameCard);
  }
}
