function display_rules(rules) {
    const container = document.getElementById("rules")
        // Set the HTML content of the new card.
    container.innerHTML = "";

  // Loop through all rules using a simple for loop
    for (let i = 0; i < rules.length; i++) {
    const rule = rules[i];

    // Extract the 'Section' and 'Description'. Since the key for description might include a leading space,
    // we use bracket notation and trim any spaces.
    const section = rule.Section || "";
    const description = (rule[" Description"] || rule.Description || "").trim();

    // Create a new element to hold this rule
    const ruleDiv = document.createElement("div");
    ruleDiv.className = "rule-item";

    // Insert the section in a header and the description in a paragraph
    ruleDiv.innerHTML = `<h4>${section}</h4><p>${description}</p>`;

    // Append the rule item to the container
    container.appendChild(ruleDiv);
  }
    
}