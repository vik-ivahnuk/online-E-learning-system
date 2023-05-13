const btn = document.getElementById("get_started");
const loginBtn = document.getElementById("log-reg");
const overlay = document.querySelector(".overlay");
const closeButtons = document.querySelectorAll(".close-button");

function showOverlay() {
    overlay.classList.remove("hidden-element");
}

function hideOverlay() {
    overlay.classList.add("hidden-element");
}

btn.addEventListener("click", showOverlay);

loginBtn.addEventListener("click", () => {
    showOverlay();
});

closeButtons.forEach((cb) => cb.addEventListener("click", () => hideOverlay()));