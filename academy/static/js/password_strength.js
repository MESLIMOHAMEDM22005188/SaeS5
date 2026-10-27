const checkBtn = document.getElementById('checkBtn');
const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');
const feedback = document.getElementById('feedback');
const crackTime = document.getElementById('crackTime');
const complexity = document.getElementById('complexity');

// Toggle password visibility
togglePassword.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Update the button label
    togglePassword.textContent = type === 'password' ? 'Show' : 'Hide';
});

// Estimate password complexity
function estimateComplexity(password) {
    const length = password.length;
    let charsetSize = 0;

    if (/[a-z]/.test(password)) charsetSize += 26; // Lowercase letters
    if (/[A-Z]/.test(password)) charsetSize += 26; // Uppercase letters
    if (/[0-9]/.test(password)) charsetSize += 10; // Digits
    if (/[\W]/.test(password)) charsetSize += 32; // Special characters

    const entropy = Math.log2(Math.pow(charsetSize, length)); // Calculated entropy
    return entropy;
}

// Format a duration in years, days, hours, and more
function formatTime(seconds) {
    if (seconds < 60) {
        return `${Math.round(seconds)} seconds`;
    } else if (seconds < 3600) {
        return `${Math.round(seconds / 60)} minutes`;
    } else if (seconds < 86400) {
        return `${Math.round(seconds / 3600)} hours`;
    } else if (seconds < 31536000) {
        return `${Math.round(seconds / 86400)} days`;
    } else {
        const years = seconds / 31536000;
        return `${Math.round(years)} years`;
    }
}

function generateComparisons(seconds) {
    const distancePerSecond = 30; // Earth travels about 30 km per second around the Sun
    const distanceTraveled = (seconds * distancePerSecond) / 1e6; // Convert to millions of kilometers

    const currentYear = new Date().getFullYear();
    const futureYear = currentYear + Math.round(seconds / 31536000);

    let comparisons = `In that time:
        - Earth would have traveled about ${distanceTraveled.toFixed(2)} million kilometers around the Sun.
        - It would now be the year ${futureYear}.`;

    if (seconds < 86400) {
        comparisons += " (Less than one day to crack this password).";
    } else if (seconds < 31536000) {
        comparisons += " (One year or less to crack it).";
    } else {
        comparisons += " (This would take a long time to crack; your password is likely strong).";
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
        feedback.textContent = 'Please enter a password.';
        feedback.className = '';
        crackTime.textContent = '';
        complexity.textContent = '';
        return;
    }

    const entropy = estimateComplexity(password);
    const seconds = estimateCrackTime(entropy);

    // Feedback utilisateur
    if (entropy < 28) {
        feedback.textContent = 'Weak password.';
        feedback.className = 'weak';
    } else if (entropy >= 28 && entropy < 60) {
        feedback.textContent = 'Moderate password.';
        feedback.className = 'medium';
    } else {
        feedback.textContent = 'Strong password.';
        feedback.className = 'strong';
    }

    crackTime.textContent = `Estimated time to crack: ${formatTime(seconds)}.`;
    complexity.textContent = `Estimated complexity: ${Math.round(entropy)} bits d'entropie.`;

    // Ajout des comparaisons
    const comparisons = generateComparisons(seconds);
    complexity.textContent += `\n${comparisons}`;
});
