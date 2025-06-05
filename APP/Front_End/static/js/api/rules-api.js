document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('ask_rules_button');
    if (button) {
        button.addEventListener('click', ask_rules);
    }
});

function ask_rules(){
    console.log("Asking for the rules...")
            fetch('/api-rules/fetch_rules')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    console.log(data.data)
                    display_rules(data.data);
                }
            })
            .catch(error => {
                console.error("Error retrieving players:", error);
            });
}