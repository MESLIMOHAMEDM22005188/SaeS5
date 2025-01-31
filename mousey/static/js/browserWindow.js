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

        var mousePosition;
        var offset = [0,0];
        var isDown = false;


        const browserWindow = document.getElementById('browser-window');
        const header = document.getElementById('browser-header');

        document.body.appendChild(browserWindow);

        header.addEventListener('mousedown', function(e) {
            isDown = true;
            offset = [
                browserWindow.offsetLeft - e.clientX,
                browserWindow.offsetTop - e.clientY
            ];
        }, true);

        document.addEventListener('mouseup', function() {
            isDown = false;
        }, true);

        document.addEventListener('mousemove', function(event) {
            event.preventDefault();
            if (isDown) {
                mousePosition = {

                    x : event.clientX,
                    y : event.clientY

                };
                browserWindow.style.left = (mousePosition.x + offset[0]) + 'px';
                browserWindow.style.top  = (mousePosition.y + offset[1]) + 'px';
            }
        }, true);



            // Gestion des événements
            document.getElementById('browser-open').addEventListener('click', openBrowserWindow);
            document.getElementById('browser-open').addEventListener('click', putBrowserInFront);
            document.getElementById('close-browser-window').addEventListener('click', closeBrowserWindow);
            document.getElementById('close-browser').addEventListener('click', closeBrowserWindow);

            document.getElementById('browser-window').addEventListener('click', putBrowserInFront);
