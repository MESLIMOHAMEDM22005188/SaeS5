const checkBtn = document.getElementById('checkBtn');
const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');
const feedback = document.getElementById('feedback');
const crackTime = document.getElementById('crackTime');
const complexity = document.getElementById('complexity');

// Fonction pour basculer l'affichage du mot de passe
togglePassword.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Changer le texte du bouton
    togglePassword.textContent = type === 'password' ? 'Afficher' : 'Masquer';
});

// Estimate password complexity
function estimateComplexity(password) {
    const length = password.length;
    let charsetSize = 0;

    if (/[a-z]/.test(password)) charsetSize += 26; // Lettres minuscules
    if (/[A-Z]/.test(password)) charsetSize += 26; // Lettres majuscules
    if (/[0-9]/.test(password)) charsetSize += 10; // Chiffres
    if (/[\W]/.test(password)) charsetSize += 32; // Special characters

    const entropy = Math.log2(Math.pow(charsetSize, length)); // Calculated entropy
    return entropy;
}

// Format a duration in years, days, hours, and more
function formatTime(seconds) {
    if (seconds < 60) {
        return `${Math.round(seconds)} secondes`;
    } else if (seconds < 3600) {
        return `${Math.round(seconds / 60)} minutes`;
    } else if (seconds < 86400) {
        return `${Math.round(seconds / 3600)} heures`;
    } else if (seconds < 31536000) {
        return `${Math.round(seconds / 86400)} jours`;
    } else {
        const years = seconds / 31536000;
        return `${Math.round(years)} years`;
    }
}

function generateComparisons(seconds) {
    const distancePerSecond = 30; // La Terre parcourt environ 30 km par seconde autour du Soleil
    const distanceTraveled = (seconds * distancePerSecond) / 1e6; // Convert to millions of kilometers

    const currentYear = new Date().getFullYear();
    const futureYear = currentYear + Math.round(seconds / 31536000);

    let comparisons = `En ce temps :
        - Earth would have traveled about ${distanceTraveled.toFixed(2)} millions de kilomètres autour du Soleil.
        - It would now be the year ${futureYear}.`;

    if (seconds < 86400) {
        comparisons += " (Moins d'un jour pour craquer ce mot de passe).";
    } else if (seconds < 31536000) {
        comparisons += " (Un an ou moins pour le craquer).";
    } else {
        comparisons += " (Beaucoup de temps pour le craquer, votre mot de passe est probablement sécurisé).";
    }

    return comparisons;
}

function estimateCrackTime(entropy) {
    const guessesPerSecond = 1e10;
    return Math.pow(2, entropy) / guessesPerSecond;
}

// Handle the click event
checkBtn.addEventListener('click', () => {
    const password = passwordInput.value.trim();

    if (!password) {
        feedback.textContent = 'Veuillez entrer un mot de passe.';
        feedback.className = '';
        crackTime.textContent = '';
        complexity.textContent = '';
        return;
    }

    const entropy = estimateComplexity(password);
    const seconds = estimateCrackTime(entropy);

    // Feedback utilisateur
    if (entropy < 28) {
        feedback.textContent = 'Mot de passe faible.';
        feedback.className = 'weak';
    } else if (entropy >= 28 && entropy < 60) {
        feedback.textContent = 'Mot de passe moyen.';
        feedback.className = 'medium';
    } else {
        feedback.textContent = 'Mot de passe fort.';
        feedback.className = 'strong';
    }

    crackTime.textContent = `Estimated time to crack: ${formatTime(seconds)}.`;
    complexity.textContent = `Estimated complexity: ${Math.round(entropy)} bits d'entropie.`;

    // Ajout des comparaisons
    const comparisons = generateComparisons(seconds);
    complexity.textContent += `\n${comparisons}`;
});
