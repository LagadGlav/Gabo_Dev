async function newPlayer() {
  const playername = document.getElementById('playernom').value;

  try {
    const res = await fetch('/api-ap/save_player', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ playername })
    });

    const payload = await res.json();

    if (!res.ok) {
      return alert(payload.error || 'Erreur inconnue du serveur');
    }

    alert(payload.message);
    console.log('Returned data :', payload.data);
  }
  catch (networkErr) {
    alert('Problème réseau ou serveur indisponible');
    console.error(networkErr);
  }
}