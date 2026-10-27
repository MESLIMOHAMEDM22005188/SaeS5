function openBrowserWindow() {
    document.getElementById('browser-window').style.display = 'block';
}

function closeBrowerWindow() {
    document.getElementById('browser-window').style.display = 'none';
}

document.getElementById('close-browser-window').addEventListener('click', closeBrowerWindow);
document.getElementById('close-browser').addEventListener('click', closeBrowerWindow);
