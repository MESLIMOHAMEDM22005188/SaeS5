document.addEventListener('DOMContentLoaded', () => {
    // Select the required HTML elements
    const submitBtn = document.getElementById('submitBtn');
    const passwordInput = document.getElementById('password');
    const feedback = document.getElementById('feedback');
    const togglePassword = document.getElementById('togglePassword');

    const porte = document.querySelector('#porte img');
    const tourDroite = document.querySelector('#tourDroite img');
    const tourGauche = document.querySelector('#tourGauche img');

    // Toggle password visibility
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePassword.textContent = type === 'password' ? 'Show' : 'Hide';
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
        return score <= 2 ? 'weak' : score === 3 || score === 4 ? 'medium' : 'strong';
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
        if (level === 'medium' && porte) porte.classList.remove('close-ico');
        if (level === 'strong') {
            if (porte) porte.classList.remove('close-ico');
            if (tourDroite) tourDroite.classList.remove('close-ico');
            if (tourGauche) tourGauche.classList.remove('close-ico');
        }
    }

    // Handle the submit button click
    if (submitBtn && passwordInput) {
        submitBtn.addEventListener('click', () => {
            const password = passwordInput.value.trim();

            if (!password) {
                feedback.textContent = 'Please enter a password.';
                feedback.className = 'error';
                return;
            }

            const strength = evaluatePassword(password);
            feedback.textContent = `Password strength: ${strength}`;
            feedback.className = strength === 'strong' ? 'success' : 'error';

            // Strengthen the fortress based on password strength
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
