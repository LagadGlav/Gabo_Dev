// Define cache keys and Time-To-Live (TTL)
const CACHE_KEY = 'allPlayers';
const CACHE_TIMESTAMP_KEY = 'allPlayersTimestamp';
const CACHE_TTL = 10 * 60 * 1000; // 10 minutes in milliseconds

// Fetch all players from API with caching
function fetchAllPlayers() {
    const now = Date.now();
    const cachedData = localStorage.getItem(CACHE_KEY);
    const cachedTimestamp = localStorage.getItem(CACHE_TIMESTAMP_KEY);

    // Use cached data if it exists and still fresh
    if (cachedData && cachedTimestamp && (now - parseInt(cachedTimestamp) < CACHE_TTL)) {
        console.log("Using cached players data.");
        const players = JSON.parse(cachedData);
        displayPlayers(players);
    } else {
        console.log("Fetching players from API...");
        fetch('/api-ap/get_all_players')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Save data and timestamp in localStorage
                    localStorage.setItem(CACHE_KEY, JSON.stringify(data));
                    localStorage.setItem(CACHE_TIMESTAMP_KEY, now.toString());
                    displayPlayers(data);
                }
            })
            .catch(error => {
                console.error("Error retrieving players:", error);
            });
    }
}
