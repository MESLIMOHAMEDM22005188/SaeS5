function openGameWindow() {
    const gameWindow = document.getElementById("game-window");
    const gameContent = document.getElementById("game-content");

    const gameTexts = [
        "Bienvenue dans le jeu !",
        "Cliquez sur les objets pour interagir.",
        "Votre objectif : découvrir l'indice caché."
    ];

    gameContent.innerHTML = ""; // Réinitialise le contenu
    gameTexts.forEach((text) => {
        const paragraph = document.createElement("p");
        paragraph.textContent = text;
        gameContent.appendChild(paragraph);
    });

    gameWindow.style.display = "block";
}

document.getElementById("close-game-window").addEventListener("click", function () {
    const gameWindow = document.getElementById("game-window");
    gameWindow.style.display = "none";
});

document.addEventListener("DOMContentLoaded", function () {
    console.log("La gestion de la fenêtre de jeu est prête.");
});
