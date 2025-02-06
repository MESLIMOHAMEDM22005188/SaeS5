const answers = [
    ["", "", "", "P", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "H", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "F", "F", "I", "R", "E", "W", "A", "L", "L", "", "", "", "", "B", "", "", "", "", "", ""],
    ["", "", "", "S", "", "", "", "N", "", "", "", "", "", "", "I", "", "", "", "", "", ""],
    ["", "", "", "H", "", "", "", "T", "", "P", "", "", "T", "R", "O", "J", "A", "N", "", "", ""],
    ["L", "O", "G", "I", "N", "", "", "I", "", "E", "", "", "", "", "M", "", "", "", "", "", ""],
    ["", "", "", "N", "", "", "", "V", "P", "N", "", "", "", "", "E", "", "", "", "", "", ""],
    ["", "", "", "G", "", "", "", "I", "", "T", "", "", "", "", "T", "", "", "", "", "D", ""],
    ["", "", "", "", "", "", "", "R", "", "E", "", "", "", "", "R", "", "", "", "", "D", ""],
    ["", "", "", "", "", "", "", "U", "", "S", "E", "C", "U", "R", "I", "S", "A", "T", "I", "O", "N"],
    ["", "", "", "", "", "", "", "S", "", "T", "", "R", "", "", "E", "", "C", "", "", "S", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "Y", "", "", "", "", "C", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "P", "", "", "", "", "E", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "T", "", "", "", "", "S", "", "", "", ""],
    ["", "", "", "", "", "", "", "S", "", "", "H", "A", "C", "K", "E", "R", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "S", "", "", "", "G", "", "", "", "A", "", "", "", "", ""],
    ["", "", "", "", "", "M", "A", "L", "W", "A", "R", "E", "", "", "", "N", "", "", "", "", ""],
    ["", "", "", "", "", "F", "", "", "", "", "", "", "", "", "", "S", "", "", "", "", ""],
    ["", "", "", "", "", "A", "", "", "", "", "", "", "", "", "R", "O", "O", "T", "K", "I", "T"],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "M", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "W", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "A", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "R", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "E", "", "", "", "", ""]
];



document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll(".crossword input");
    const hintButton = document.getElementById("hint-button");
    const validateButton = document.getElementById("validate-button");
    const resetButton = document.getElementById("reset-button");

const getInputCoordinates = (input) => {
    const row = parseInt(input.dataset.row, 10);
    const col = parseInt(input.dataset.col, 10);
    return { row, col };
};
validateButton.addEventListener("click", () => {
    inputs.forEach((input, index) => {
        const { row, col } = getInputCoordinates(input);
        const userAnswer = input.value.trim().toUpperCase(); // Nettoie l'entrée utilisateur

        console.log(`Index: ${index}, Row: ${row}, Col: ${col}, Expected: ${answers[row][col]}, Input: ${userAnswer}`);

        // Si la case n'a pas de réponse attendue dans le tableau, ne rien faire
        if (!answers[row] || answers[row][col] === "") {
            input.style.backgroundColor = ""; // Réinitialiser la couleur pour les cases sans réponse
            return;
        }

       if (userAnswer === "") {
    input.style.backgroundColor = "blue"; // Réinitialise la couleur si l'input est vide
} else if (userAnswer === answers[row][col]) {
    input.style.backgroundColor = "lightgreen"; // Bonne réponse
} else {
    input.style.backgroundColor = "lightcoral"; // Mauvaise réponse
}


    });
});



    resetButton.addEventListener("click", () => {
        inputs.forEach(input => {
            input.value = "";
            input.style.backgroundColor = ""; // Réinitialiser les couleurs
        });
    });

    hintButton.addEventListener("click", () => {
        let randomIndex;
        do {
            randomIndex = Math.floor(Math.random() * inputs.length);
            const { row, col } = getInputCoordinates(randomIndex);
            if (answers[row] && answers[row][col] !== "") {
                const input = inputs[randomIndex];
                input.value = answers[row][col]; // Remplir la réponse correcte
                input.style.backgroundColor = "lightblue"; // Indication visuelle
                break;
            }
        } while (true);
    });
});
