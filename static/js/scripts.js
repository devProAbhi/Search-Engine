
// Responsive navigation
var navbar = document.querySelector(".navbar");
var menuToggle = document.querySelector(".menu-toggle");

menuToggle.addEventListener("click", function () {
    navbar.classList.toggle("open");
});


// Close navigation menu on link click
var navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
        navbar.classList.remove("open");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const days = document.querySelectorAll(".day");
    const eventDetails = document.getElementById("event-details");

    days.forEach(function (day) {
        day.addEventListener("click", function () {
            const contestName = this.querySelector(".contest").textContent;
            eventDetails.textContent = `Contest: ${contestName}`;
        });
    });
});





