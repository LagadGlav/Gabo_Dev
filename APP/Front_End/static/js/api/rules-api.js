document.addEventListener('DOMContentLoaded', function() {
    const languageButtons = [
        { id: 'ask_rules_button', lang: 'en' },
        { id: 'ask_rules_button_es', lang: 'es' },
        { id: 'ask_rules_button_fr', lang: 'fr' },
        { id: 'ask_rules_button_bzh', lang: 'bzh' },
        { id: 'ask_rules_button_eus', lang: 'eus' }
    ];

    languageButtons.forEach(btn => {
        const button = document.getElementById(btn.id);
        if (button) {
            button.addEventListener('click', function() {
                fetchRules(btn.lang);
            });
        }
    });
});

function fetchRules(lang) {
    console.log(`Requesting rules in ${lang}`);
    fetch(`/api-rules/fetch_rules?lang=${lang}`)
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              alert(data.error);
          } else {
              console.log(data.data);
              display_rules(data.data); // send to rules-display.js
          }
      })
      .catch(error => {
          console.error("Error retrieving rules:", error);
      });
}
