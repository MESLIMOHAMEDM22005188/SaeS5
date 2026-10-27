//récupération de l'horloge
let clock = document.querySelector('.clock')
let date = document.querySelector('.date')

//fonction de mise à jour de l'horloge
function updateTime() {
    //récupération de l'heure et les minutes du systeme
    let hours = new Date().getHours();
    let minutes = new Date().getMinutes();
    let day = new Date().getDay();
    let month = new Date().getMonth();
    let year = new Date().getFullYear();

    //ajout d'un 0 avant le chiffre dans le cas ou l'heure ou les valeurs sont inferieur à 10
    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    day = day < 10 ? "0" + day : day;
    month = month <10? "0" + month : month;


    //modification du div pour mettre l'heure du systeme
    clock.innerHTML = `${hours}:${minutes}`;
    date.innerHTML = `${day}/${month}/${year}`;

    //appel de la fonction toutes les 60 secondes
    //comme le timer commence au moment du lancement de la  page, un décallage
    //sera présent par rapport au temps réel. C'est un choix personnel
    //pour éviter d'appeler 59 fois /minutes la fonction sans effectuer de changement
    setTimeout(updateTime, 60000);
}

updateTime();

//Control du volume
document.addEventListener("DOMContentLoaded", () => {
  const range = document.querySelector(".volume input[type=range]");

  const barHoverBox = document.querySelector(".volume .bar-hoverbox");
  const fill = document.querySelector(".volume .bar .bar-fill");

  range.addEventListener("change", (e) => {
    console.log("value", e.target.value);
  });

  const setValue = (value) => {
    fill.style.width = value + "%";
    range.setAttribute("value", value)
    range.dispatchEvent(new Event("change"))
  }

  // Дефолт
  setValue(range.value);

  const calculateFill = (e) => {
    // Отнимаем ширину двух 15-пиксельных паддингов из css
    let offsetX = e.offsetX

    if (e.type === "touchmove") {
      offsetX = e.touches[0].pageX - e.touches[0].target.offsetLeft
    }

    const width = e.target.offsetWidth - 30;

    setValue(
      Math.max(
        Math.min(
          // Отнимаем левый паддинг
          (offsetX - 15) / width * 100.0,
          100.0
        ),
        0
      )
    );
  }

  let barStillDown = false;

  barHoverBox.addEventListener("touchstart", (e) => {
    barStillDown = true;

    calculateFill(e);
  }, true);

  barHoverBox.addEventListener("touchmove", (e) => {
    if (barStillDown) {
      calculateFill(e);
    }
  }, true);

  barHoverBox.addEventListener("mousedown", (e) => {
    barStillDown = true;

    calculateFill(e);
  }, true);

  barHoverBox.addEventListener("mousemove", (e) => {
    if (barStillDown) {
      calculateFill(e);
    }
  });

  barHoverBox.addEventListener("wheel", (e) => {
    const newValue = +range.value + e.deltaY * 0.5;

    setValue(Math.max(
      Math.min(
        newValue,
        100.0
      ),
      0
    ))
  });

  document.addEventListener("mouseup", (e) => {
    barStillDown = false;
  }, true);

  document.addEventListener("touchend", (e) => {
    barStillDown = false;
  }, true);
})

let isToggled = false;

function toggleVolumeSlider() {
    const volumePopup = document.getElementById('volume-popup');
    if (!isToggled) {
        isToggled = true;
        volumePopup.style.display = "block";
    }else{
        isToggled = false;
        volumePopup.style.display = "none";
    }

}