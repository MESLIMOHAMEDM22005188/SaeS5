
let points = 0;
const emails = [
    {
        id: 1,
        sender: "ruuqn44Jrf@gmiel.com",
        subject: "Gagnez une tablette Apple !",
        body: "Congratulations! You were selected from 100,000 entrants to win a tablet. Click here to claim your prize: <a href='http://win-free-apple-not-v1ru5.co'>http://win-free-apple-not-v1ru5.co</a>",
        isPhishing: true,
        reported: false
    },
    {
        id: 2,
        sender: "secretaire-cybermouse@gmiel.com",
        subject: "Warning: Security issue",
        body: "Hello,<br><br>Several students have recently been targeted by phishing. Stay alert and avoid suspicious links.<br><br>Thank you, the school office.",
        isPhishing: false,
        reported: false
    },
    {
        id: 3,
        sender: "secretalre-cybermouse@gmiel.com",
        subject: "Training: Learn to detect phishing",
        body: "Hello,<br><br>Here is the link to phishing-awareness training: <a href='http://formation-phishing-1.com'>http://formation-phishing-1.com</a>",
        isPhishing: true,
        reported: false
    },
    {
        id: 4,
        sender: "service-technique-cybermouse@gmiel.com",
        subject: "Network maintenance",
        body: "Hello,<br><br>Following a network incident, some internet searches may fail.<br>We are working to resolve the issue as quickly as possible.<br>Thank you for your patience.<br><br>Technical support",
        isPhishing: false,
        reported: false
    }
];

// Restore the emails and reset the score:
// saveEmails();
// savePoints();


// Functions for email UI and DOM rendering

function openEmailWindow() {
    document.getElementById('email-window').style.display = 'block';
    loadEmailTitles();
}

function closeEmailWindow() {
    document.getElementById('email-window').style.display = 'none';
}

function loadEmailTitles() {
    const emailTitles = document.getElementById('email-titles');
    emailTitles.innerHTML = '';

    emails.forEach(email => {
        const listItem = document.createElement('li');
        listItem.textContent = `${email.sender} - ${email.subject}`;
        listItem.setAttribute('data-id', email.id);

        if (email.reported) {
            listItem.style.backgroundColor = email.isPhishing ? 'green' : 'red';
        }

        listItem.addEventListener('click', () => displayEmailContent(email.id));
        emailTitles.appendChild(listItem);
    });
}

function displayEmailContent(emailId) {
    const email = emails.find(e => e.id === emailId);
    const emailContent = document.getElementById('email-content');
    emailContent.innerHTML = `
        <p class="email-Plus">
            <img src="/static/image/more_options.png" class="plus-Option" onclick="openMoreOption(event, ${email.id})">
        </p>
        <p class="email-Sender"><strong>De :</strong> ${email.sender}</p>
        <p class="email-Object"><strong>Objet :</strong> ${email.subject}</p>
        <p>${email.body}</p>
        <div id="email-options-${email.id}" class="email-options">
            <button onclick="markAsUnread(${email.id})">Mark as unread</button>
            <button onclick="deleteEmail(${email.id})">Delete</button>
            <button onclick="reportEmail(${email.id})">Report</button>
        </div>
    `;

    // Handle clicks on suspicious links
    const links = emailContent.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopImmediatePropagation();
            console.log('Link clicked!');
            if (email.isPhishing) {
                triggerPhishingPopups(emailId);
            } else {
                alert("This link is legitimate. No action is required.");
            }
        });
    });
}


function triggerPhishingPopups(emailId) {
    if (document.querySelector('.hacked-message')) return;
    points -= 100;
    savePoints();

    document.body.style.pointerEvents = 'none';

    const popupContainer = document.createElement('div');
    popupContainer.classList.add('popup-container');
    document.body.appendChild(popupContainer);

    let delay = 500;
    const minDelay = 30;
    let count = 0;
    const maxPopups = 100;

    function getRandomPosition() {
        const top = Math.random() * 90 - 5;
        const left = Math.random() * 90 - 5;
        return {top: `${top}%`, left: `${left}%`};
    }

    function createPopup() {
        const popup = document.createElement('div');
        popup.classList.add('popup');
        const {top, left} = getRandomPosition();
        popup.style.top = top;
        popup.style.left = left;
        popup.innerHTML = `
            <h1>Piratage en cours...</h1>
            <p>Please do not turn off your computer.</p>
        `;
        popupContainer.appendChild(popup);

        delay = Math.max(minDelay, delay * 0.9);
        count++;

        if (count < maxPopups) {
            setTimeout(createPopup, delay);
        }
    }

    createPopup();

    setTimeout(() => {
        const blueScreen = document.createElement('div');
        blueScreen.style.position = 'fixed';
        blueScreen.style.top = '0';
        blueScreen.style.left = '0';
        blueScreen.style.width = '100vw';
        blueScreen.style.height = '100vh';
        blueScreen.style.backgroundImage = 'url("/static/image/blue_screen.png")';
        blueScreen.style.backgroundSize = 'cover';
        blueScreen.style.zIndex = '9999';
        blueScreen.classList.add('blue-screen');
        document.body.appendChild(blueScreen);

        setTimeout(() => {
            blueScreen.remove();
            popupContainer.remove();
            document.body.innerHTML = `
                <div class="hacked-message" style="text-align: center; padding: 50px;">
                    <h1>Session restarted</h1>
                    <p>You were hacked! Do not click suspicious links.</p>
                    <p><strong>Hint:</strong> Check the sender's email address and the URL.</p>
                    <button onclick="reloadSession()" style="padding: 10px 20px; font-size: 16px;">Try again</button>
                </div>
            `;
            document.body.style.pointerEvents = 'auto';
        }, 3000);
    }, 6800);
}

function reloadSession() {
    location.reload();
    updatePointsDisplay();
}


// Email management functions

function reportEmail(emailId) {
    const email = emails.find(e => e.id === emailId);
    const emailElement = document.querySelector(`[data-id="${emailId}"]`);

    if (email.reported) {
        alert("This email has already been reported.");
        return;
    }

    email.reported = true;

    if (email.isPhishing) {
        emailElement.style.backgroundColor = 'green';
        alert("Correct! You reported a phishing email. You can now delete it.");
        points += 100;
    } else {
        emailElement.style.backgroundColor = 'red';
        alert("You reported a legitimate email. Your credibility has decreased.");
        points -= 100;
    }

    savePoints();
    saveEmails();
    updatePointsDisplay();
    checkAllPhishingReported();
}

function deleteEmail(emailId) {
    const emailIndex = emails.findIndex(e => e.id === emailId);

    if (emails[emailIndex].reported && emails[emailIndex].isPhishing) {
        emails.splice(emailIndex, 1);
        const emailElement = document.querySelector(`[data-id="${emailId}"]`);
        emailElement.remove();
        document.getElementById('email-content').innerHTML = '';
        alert("The email was deleted successfully.");
        saveEmails();
    } else if (emails[emailIndex].reported && !emails[emailIndex].isPhishing) {
        alert("This email is legitimate and cannot be deleted.");
    } else {
        alert("You must correctly report this email before deleting it.");
    }
}


// Score functions

function savePoints() {
    sessionStorage.setItem('points', points);
}

function loadPoints() {
    const savedPoints = sessionStorage.getItem('points');
    points = savedPoints !== null ? parseInt(savedPoints, 10) : 0;
}

function updatePointsDisplay() {
    const pointsDisplay = document.querySelector('.points-display');
    pointsDisplay.textContent = `Points: ${points}`;
}


// Data management functions

function loadEmails() {
    const savedEmails = JSON.parse(sessionStorage.getItem('emails'));
    if (savedEmails) {
        emails.length = 0;
        emails.push(...savedEmails);
    }
}

function saveEmails() {
    sessionStorage.setItem('emails', JSON.stringify(emails));
}


// Additional options

function openMoreOption(event, emailId) {
    event.stopPropagation();
    const options = document.getElementById(`email-options-${emailId}`);

    if (options.classList.contains('visible')) {
        options.classList.remove('visible');
        options.style.left = '';
        options.style.top = '';
        return;
    }

    const rect = event.target.getBoundingClientRect();

    options.style.position = 'fixed';
    options.style.left = `${rect.left - options.offsetWidth - 135}px`;
    options.style.top = `${rect.bottom + 3}px`;
    options.classList.add('visible');
}


// Track successful phishing reports

function checkAllPhishingReported() {
    const allReported = emails.every(email => !email.isPhishing || email.reported);
    if (allReported) {
        sendCongratulationsMail();
        sendChallenge2Mail();
    }
}

function sendCongratulationsMail() {
    const congratulationsEmail = {
        id: 5,
        sender: "admin@cybersecure.com",
        subject: "Congratulations on staying alert!",
        body: `
            Great job! You successfully reported all phishing emails!<br>
            You completed the first challenge in this level.
        `,
        read: false,
        isPhishing: false,
        reported: false
    };

    emails.push(congratulationsEmail);
    saveEmails();
    loadEmailTitles();
}

function sendChallenge2Mail() {
    const challenge2Email = {
        id: 6,
        sender: "collegue@cybersecure.com",
        subject: "Project update",
        body: `
            The project has been updated and now requires Flowtouch version 3.21.6 <br>
            Install the update before resuming the project.
        `,
        read: false,
        isPhishing: false,
        reported: false
    };

    emails.push(challenge2Email);
    saveEmails();
    loadEmailTitles();
}

// Initialize and manage events

document.getElementById('close-email-window').addEventListener('click', closeEmailWindow);

document.addEventListener('DOMContentLoaded', () => {
    loadEmails();
    loadPoints();
    loadEmailTitles();
    updatePointsDisplay();

    setTimeout(() => {
        const phishingMessage = document.getElementById('phishing-message');
        phishingMessage.style.display = 'block';
    }, 30000);
});


document.addEventListener('click', () => {
    document.querySelectorAll('.email-options.visible').forEach(menu => {
        menu.classList.remove('visible');
        menu.style.left = '';
        menu.style.top = '';
    });
});

// Bring the email window to the foreground
function putEmailInFront() {
    const emailWindow = document.getElementById('email-window');
    const browserWindow = document.getElementById('browser-window');
    if (emailWindow) {
        emailWindow.style.zIndex = '100';
        const childrenEmail = emailWindow.querySelectorAll('*');
        childrenEmail.forEach(child => {
            child.style.zIndex = '100';
        });

        browserWindow.style.zIndex = '1';
        const childrenBrowser = browserWindow.querySelectorAll('*');
        childrenBrowser.forEach(child => {
            child.style.zIndex = '1';
        });
    }
    putBrowserInBack()
}

// Send the email window to the background
function putEmailInBack() {
    const emailWindow = document.getElementById('email-window');
    if (emailWindow) {
        emailWindow.style.zIndex = '1'; // Send the email to the background
    }
}

var mousePositionEmail;
var offsetEmail = [0, 0];
var isDownEmail = false;


const emailWindow = document.getElementById('email-window');
const headerEmail = document.getElementById('email-header');

document.body.appendChild(emailWindow);

headerEmail.addEventListener('mousedown', function (e) {
    isDownEmail = true;
    offsetEmail = [
        emailWindow.offsetLeft - e.clientX,
        emailWindow.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function () {
    isDownEmail = false;
}, true);

document.addEventListener('mousemove', function (event) {
    event.preventDefault();
    if (isDownEmail) {
        mousePositionEmail = {
            x: event.clientX,
            y: event.clientY
        };
        emailWindow.style.left = (mousePositionEmail.x + offsetEmail[0]) + 'px';
        emailWindow.style.top = (mousePositionEmail.y + offsetEmail[1]) + 'px';
    }
}, true);

// Add event listeners for opening and managing emails
document.getElementById('email-open').addEventListener('click', openEmailWindow);
document.getElementById('email-open').addEventListener('click', putEmailInFront);
document.getElementById('email-window').addEventListener("click", putEmailInFront);
