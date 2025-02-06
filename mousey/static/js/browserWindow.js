// Ouvre la fenêtre du navigateur
function openBrowserWindow() {
    const browserWindow = document.getElementById('browser-window');
    if (browserWindow) {
        browserWindow.style.display = 'block';
        browserWindow.style.zIndex = '100';
    }
}

// Ferme la fenêtre du navigateur
function closeBrowserWindow() {
    const browserWindow = document.getElementById('browser-window');
    if (browserWindow) {
        browserWindow.style.display = 'none';
    }
}

// Mets le navigateur en avant
function putBrowserInFront() {
    const browserWindow = document.getElementById('browser-window');
    const emailWindow = document.getElementById('email-window');
    if (browserWindow && emailWindow) {
        browserWindow.style.zIndex = '100';
        const childrenBrowser = browserWindow.querySelectorAll('*');
        childrenBrowser.forEach(child => {
            child.style.zIndex = '100';
        });

        emailWindow.style.zIndex = '1';
        const childrenEmail = emailWindow.querySelectorAll('*');
        childrenEmail.forEach(child => {
            child.style.zIndex = '1';
        });

        putEmailInBack();
    }
}

// Mets l'email en arrière
function putBrowserInBack() {
    const browserWindow = document.getElementById('browser-window');
    if (browserWindow) {
        browserWindow.style.zIndex = '1';
        const childrenBrowser = browserWindow.querySelectorAll('*');
        childrenBrowser.forEach(child => {
            child.style.zIndex = '1';
        });
    }
}


//Systeme de déplacement de la fenetre web
var mousePosition;
var offset = [0, 0];
var isDown = false;


const browserWindow = document.getElementById('browser-window');
const header = document.getElementById('browser-header');

document.body.appendChild(browserWindow);

header.addEventListener('mousedown', function (e) {
    isDown = true;
    offset = [
        browserWindow.offsetLeft - e.clientX,
        browserWindow.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function () {
    isDown = false;
}, true);

document.addEventListener('mousemove', function (event) {
    event.preventDefault();
    if (isDown) {
        mousePosition = {

            x: event.clientX,
            y: event.clientY

        };
        browserWindow.style.left = (mousePosition.x + offset[0]) + 'px';
        browserWindow.style.top = (mousePosition.y + offset[1]) + 'px';
    }
}, true);

//Fin systeme de déplacement de fenetre web


function search(searchBar) {
    if (event.key === 'Enter') {
        const centerImg = document.getElementById('centerImg');
        const browserContent = document.getElementById('browser-content');
        if (searchBar.value.toLowerCase().includes("flowtouch")) {
            loadSearchFlowtouch();
        } else {
            browserContent.innerHTML = `
        <img src="/static/image/erreurConnexion.png" id="centerImg" style="padding-left: 40%">
        <div style="color: white;padding-left: 45%">Connexion instable.</div> 
        <div style="color: white;padding-left: 33%"> <br> Veuillez contacter votre service technique pour plus d'information</div>
        `;
            centerImg.style.display = "block";
        }
    }
}

function loadSearchFlowtouch() {
    const browserContent = document.getElementById('browser-content');
    const centerImg = document.getElementById('centerImg');

    centerImg.style.display = "none";
    browserContent.innerHTML = `
                        <div id="search-results">
                            <div style="display: flex; flex-direction: row">
                                <leftSide style="padding-right: 700px">
                                    <h2 style="padding-left: 50px">Résultats pour "Flowtouch"</h2>
                                    <ul style="list-style-type: none; padding-left: 100px;">
                                        <site1 style="margin-bottom: 20px; cursor: pointer" onclick="loadFirstFlowtouchLink()">
                                            <upperPart style="display: flex; align-items: center; margin-bottom: 10px;">
                                                <img src="/static/image/flowtouchLogo.png" width="30" height="30" alt="Flowtouch Logo" style="margin-right: 10px;">
                                                <div class="text">
                                                    <p style="margin: 0; font-weight: bold; font-size: 0.8em;">Flowt0uch</p>
                                                    <div font-size: 0.5em;">http://flowt0uch.com > download</div>
                                                </div>
                                            </upperPart>
                                            <lowerPart>
                                                <siteTitle style="font-size: 1.0em; color: #1a73e8">
                                                    Télécharger Flowtouch gratuitement <br>
                                                </siteTitle>
                                                <description style="font-size: 0.7em">
                                                    Télécharger la dernière version du logiciel gratuit Flowtouch ... <br> <br> <br>
                                                </description>
                                            </lowerPart>
                                        </site1 >
                                        <site2 style="margin-bottom: 15px; cursor: pointer" onclick="loadSecondFlowtouchLink()">
                                            <upperPart style="display: flex; align-items: center; margin-bottom: 10px;">
                                                <img src="/static/image/flowtouchLogo.png" width="30" height="30" alt="Flowtouch Logo" style="margin-right: 10px;">
                                                <div class="text">
                                                    <p style="margin: 0; font-weight: bold; font-size: 0.8em;">Flowtouch - Site officiel</p>
                                                    <div font-size: 0.5em;">http://flowtouch.com > download</div>
                                                </div>    
                                            </upperPart>
                                            <lowerPart>
                                                <siteTitle style="font-size: 1.0em; color: #1a73e8;">
                                                    Flowtouch <br>
                                                </siteTitle>
                                                <description style="font-size: 0.7em">
                                                    Découvrez Flowtouch, un logiciel passif opensource de ... <br> <br> <br>
                                                </description>
                                            </lowerPart>
                                        </site2>
                                        <site3 style="margin-bottom: 15px; cursor: pointer" onclick="loadThirdFlowtouchLink()">
                                            <upperPart style="display: flex; align-items: center; margin-bottom: 10px;">
                                                <img src="/static/image/flowtouchLogo.png" width="30" height="30" alt="Flowtouch Logo" style="margin-right: 10px;">
                                                <div class="text">
                                                    <p style="margin: 0; font-weight: bold; font-size: 0.8em;">Télécharger Flowtouch</p>
                                                    <div font-size: 0.5em;">http://telecharger-flowtouch.com</div>
                                                </div>  
                                            </upperPart>
                                            <lowerPart>
                                                <siteTitle style="font-size: 1.0em; color: #1a73e8;">
                                                    Télécharger flowtouch 3.20.57 <br>
                                                </siteTitle>
                                                <description style="font-size: 0.7em">
                                                    Télécharger les archives ou la derniere version de Flowtouch ... <br> <br> <br>
                                                </description>
                                            </lowerPart>
                                        </site3>
                                    </ul>
                                </leftSide>
                                <rightSide style="right: 0; border: #232323; border-radius: 10px; background: #7a7a7a">
                                    <h3 style="font-size: 1.2em; font-weight: bold;">À propos de Flowtouch</h3>
                                        <img src="/static/image/flowtouchLogo.png" width="100" height="100" alt="Flowtouch Logo" style="margin-bottom: 10px; display: block; padding-left: 75px">
                                        <p style="font-size: 0.9em; line-height: 1.4em;">
                                            Flowtouch est un logiciel innovant <br> conçu pour améliorer l'efficacité des <br> utilisateurs grâce à des fonctionnalités <br> intuitives et un design minimaliste.
                                        </p>
                                        <p style="font-size: 0.9em; font-weight: bold;">Site officiel :</p>
                                        <p style="font-size: 0.9em; color: #1a73e8;">http://flowtouch.com</p>
                                        <p style="font-size: 0.9em;">Téléchargez la dernière version de <br> Flowtouch gratuitement pour bénéficier <br> des dernières fonctionnalités.</p>
                                </rightSide>
                            </div>
                        </div>
                    `;
}

function loadFirstFlowtouchLink() {
    const browserContent = document.getElementById('browser-content');

    browserContent.innerHTML = `
                        <div style="background: white; width: 100%; height: 100%" > 
                            <div style="margin-left: 34%;padding-top: 13%; color: #1a1a1a; font-size: 30px">
                                <strong>Télécharger Flowtouch 3.21.6</strong>
                                <br>
                                <br>
                                <div style="margin-left: 17%">
                                    <button onclick="triggerPhishingPopups()" id="download-link-1"> Télécharger</button>
                                </div>
                            </div>
                        </div>
                    `;
}

function loadSecondFlowtouchLink() {
    const browserContent = document.getElementById('browser-content');

    browserContent.innerHTML = `
                        <div class="container">
                            <img src="/static/image/flowtouchLogo.png" alt="FlowTouch Logo" class="logo">
                            <h1>Bienvenue sur FlowTouch</h1>
                            <p>L'outil ultime pour les développeurs, optimisé pour un workflow fluide et efficace.</p>
                            <button onclick="()" class="download-button">Télécharger FlowTouch</button>
                        </div>
                         
                    `;
}

function loadThirdFlowtouchLink() {
    const browserContent = document.getElementById('browser-content');

    browserContent.innerHTML = `
                        <div class="container">
                            <h1>Bienvenue sur FlowTouch</h1>
                            <p>L'outil ultime pour les développeurs, optimisé pour un workflow fluide et efficace.</p>
                            <button onclick="triggerPhishingPopups()" class="download-button">Télécharger FlowTouch</button>
                        </div>
                    `;
}


// Gestion des événements
document.getElementById('browser-open').addEventListener('click', openBrowserWindow);
document.getElementById('browser-open').addEventListener('click', putBrowserInFront);
document.getElementById('close-browser-window').addEventListener('click', closeBrowserWindow);
document.getElementById('close-browser').addEventListener('click', closeBrowserWindow);
document.getElementById('browser-window').addEventListener('click', putBrowserInFront);
