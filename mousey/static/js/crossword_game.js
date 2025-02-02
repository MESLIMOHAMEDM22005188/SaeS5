document.addEventListener("DOMContentLoaded", function() {
    // Réponses correctes pour les mots croisés
    const correctAnswers = {
        "1-1": "P",
        "1-2": "H",
        "1-3": "I",
        "1-4": "S",
        "1-5": "H",
        "1-6": "I",
        "1-7": "N",
        "2-1": "M",
        "2-2": "A",
        "2-3": "L",
        "2-4": "W",
        "2-5": "A",
        "2-6": "R",
        "2-7": "E",
        "3-1": "M",
        "3-2": "A",
        "3-3": "L",
        "3-4": "W",
        "3-5": "A",
        "3-6": "R",
        "3-7": "E"
    };

    const checkButton = document.getElementById("check-button");
    const message = document.getElementById("message");

    // Vérification des réponses
    checkButton.addEventListener("click", function() {
        let correctCount = 0;

        for (const id in correctAnswers) {
            const inputElement = document.getElementById(id);
            if (inputElement.value.toUpperCase() === correctAnswers[id]) {
                correctCount++;
            }
        }

        // Vérifier si toutes les réponses sont correctes
        if (correctCount === Object.keys(correctAnswers).length) {
            message.textContent = "Félicitations ! Vous avez complété le mot croisé correctement.";
            message.style.color = "green";
        } else {
            message.textContent = "Il y a encore des erreurs, réessayez.";
            message.style.color = "red";
        }
    });
});
