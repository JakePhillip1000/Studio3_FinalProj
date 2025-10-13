document.addEventListener("DOMContentLoaded", function () {
    const addEventBtn = document.querySelector(".add-event-btn");
    const popUp = document.getElementById("popupOverlay");
    const quitBtn = popUp.querySelector(".quit-btn");
    const addEventForm = document.getElementById("addEventForm");

    if (!addEventBtn || !popUp || !quitBtn || !addEventForm) {
        return;
    }

    addEventBtn.addEventListener("click", function () {
        popUp.classList.remove("hidden");
        popUp.style.display = "flex"; 
        document.body.classList.add("popup-open");
    });

    quitBtn.addEventListener("click", function () {
        addEventForm.reset();
        popUp.classList.add("hidden");
        popUp.style.display = "none";
        document.body.classList.remove("popup-open");
    });

    let deleteForms = document.querySelectorAll(".delete-event-form");
    for (var i = 0; i < deleteForms.length; i++) {
        deleteForms[i].addEventListener("submit", function (event) {
            var confirmDelete = confirm("Are you sure deleting this event?");
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    }
});
