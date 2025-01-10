// Fonctions liées à l'affichage du navigateur (UI/DOM)

function openBrowserWindow() {
    document.getElementById('browser-window').style.display = 'block';
}

function closeBrowerWindow() {
    document.getElementById('browser-window').style.display = 'none';
}

// Initialisation et gestion des événements

document.getElementById('close-browser-window').addEventListener('click', closeBrowerWindow);
document.getElementById('close-browser').addEventListener('click', closeBrowerWindow);