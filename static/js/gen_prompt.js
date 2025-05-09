document.getElementById("generatePromptText").addEventListener("click", () => {
    const options = document.getElementById("promptOptions");
    options.classList.toggle("show");
  });

document.getElementById("generatePromptBtn").addEventListener("click", async () => {
    const selected = document.querySelector('input[name="prompt"]:checked');
    if (!selected) return alert("Please select a prompt difficulty level");

    const response = await fetch("/generate_prompt", {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({ level: selected.value })
    });

    const data = await response.json();
    if (data.prompt) {
        document.getElementById("journalTitle").value = data.prompt;
    }
});
  