async function fetchLastTenGames(playerId) {
    try {
        // Notice the API prefix (/api-ag/) used to call the dedicated API service
        const response = await fetch(`/api-ap/player/${playerId}/last-games`);
        if (!response.ok) {
            throw new Error(`Network response was not ok (Status: ${response.status})`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching last ten games:', error);
        return null;
    }
}
