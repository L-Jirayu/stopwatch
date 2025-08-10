let timerDisplay = document.getElementById("timer");
let startBtn = document.getElementById("start");
let pauseBtn = document.getElementById("pause");
let resetBtn = document.getElementById("reset");

let startTime = 0;
let elapsedTime = 0;
let timerInterval;
let isRunning = false;

let activityText = document.getElementById("activityText");
function safeSetTextContent(el, text) {
  if (el) el.textContent = text;
}

function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  const centiseconds = String(Math.floor((ms % 1000) / 10)).padStart(2, "0");
  return `${minutes}:${seconds}:${centiseconds}`;
}

function updateDisplay() {
  timerDisplay.textContent = formatTime(elapsedTime);
}

startBtn.addEventListener("click", () => {
  if (!isRunning) {
    safeSetTextContent(activityText, '');

    startTime = Date.now() - elapsedTime;
    timerInterval = setInterval(() => {
      elapsedTime = Date.now() - startTime;
      updateDisplay();
    }, 10);
    isRunning = true;
  }
});

pauseBtn.addEventListener("click", () => {
  clearInterval(timerInterval);
  isRunning = false;
  fetchQuote()
});

resetBtn.addEventListener("click", () => {
  clearInterval(timerInterval);
  isRunning = false;
  elapsedTime = 0;
  updateDisplay();
  safeSetTextContent(activityText, '');
});

function fetchQuote() {
  fetch("https://api.quotable.io/random")
    .then(response => response.json())
    .then(data => {
      safeSetTextContent(activityText, data.content);
    })
    .catch(error => {
      console.error("Error fetching quote:", error);
      safeSetTextContent(activityText, "เกิดข้อผิดพลาดในการดึงข้อมูล");
    });
}
