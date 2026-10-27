document.addEventListener('DOMContentLoaded', () => {
    // Select the required HTML elements
    const submitBtn = document.getElementById('submitBtn');
    const passwordInput = document.getElementById('password');
    const feedback = document.getElementById('feedback');
    const togglePassword = document.getElementById('togglePassword');

    const porte = document.querySelector('#porte img');
    const tourDroite = document.querySelector('#tourDroite img');
    const tourGauche = document.querySelector('#tourGauche img');

    // Toggle pour afficher/masquer le mot de passe
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePassword.textContent = type === 'password' ? 'Afficher' : 'Masquer';
        });
    }

    // Evaluate password complexity
    function evaluatePassword(password) {
        let score = 0;
        if (password.length >= 8) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[\W]/.test(password)) score++;
        return score <= 2 ? 'faible' : score === 3 || score === 4 ? 'moyen' : 'fort';
    }

    // Reset the fortress
    function resetFortress() {
        if (porte) porte.classList.add('close-ico');
        if (tourDroite) tourDroite.classList.add('close-ico');
        if (tourGauche) tourGauche.classList.add('close-ico');
    }

    // Strengthen the fortress based on password strength
    function reinforceFortress(level) {
        resetFortress();
        if (level === 'moyen' && porte) porte.classList.remove('close-ico');
        if (level === 'fort') {
            if (porte) porte.classList.remove('close-ico');
            if (tourDroite) tourDroite.classList.remove('close-ico');
            if (tourGauche) tourGauche.classList.remove('close-ico');
        }
    }

    // Gestion du clic sur le bouton de soumission
    if (submitBtn && passwordInput) {
        submitBtn.addEventListener('click', () => {
            const password = passwordInput.value.trim();

            if (!password) {
                feedback.textContent = 'Veuillez entrer un mot de passe.';
                feedback.className = 'error';
                return;
            }

            const strength = evaluatePassword(password);
            feedback.textContent = `Password strength: ${strength}`;
            feedback.className = strength === 'fort' ? 'success' : 'error';

            // Renforcement de la forteresse selon le mot de passe
            reinforceFortress(strength);
        });
    }

    // Reset the game on restart
    const restartButton = document.getElementById('restart-button');
    if (restartButton) {
        restartButton.addEventListener('click', () => {
            if (passwordInput) passwordInput.value = '';
            if (feedback) {
                feedback.textContent = '';
                feedback.className = '';
            }
            resetFortress();
        });
    }

    // Redirection vers le menu
    const backToMenuButton = document.getElementById('back-to-menu');
    if (backToMenuButton) {
        backToMenuButton.addEventListener('click', () => {
            window.location.href = '/level-two/';
        });
    }
});
