const hamburger_menu = document.querySelector(".dropdown-menu");
const navbar = document.querySelector("header nav");
const links = document.querySelectorAll(".links a");
const btn = document.querySelector(".btn");
const loginBtn = document.querySelector(".log-reg-btn");
const overlay = document.querySelector(".overlay");
const closeButtons = document.querySelectorAll(".close-button");

function closeMenu() {
    navbar.classList.remove("open");
    document.body.classList.remove("scroll-none");
}

function showOverlay() {
    overlay.classList.remove("hidden-element");
}

function hideOverlay() {
    overlay.classList.add("hidden-element");
}

hamburger_menu.addEventListener("click", () => {
    if (!navbar.classList.contains("open")) {
        navbar.classList.add("open");
        document.body.classList.add("scroll-none");
    } else {
        closeMenu();
    }
});

btn.addEventListener("click", showOverlay);

loginBtn.addEventListener("click", () => {
    closeMenu();
    showOverlay();
});

closeButtons.forEach((cb) => cb.addEventListener("click", () => hideOverlay()));
links.forEach((link) => link.addEventListener("click", () => closeMenu()));