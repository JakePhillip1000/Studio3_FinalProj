window.addEventListener("DOMContentLoaded", function () {
    const userImg = document.getElementById("user-img");
    const userMenu = document.getElementById("user-menu");
    const logoutBtn = document.getElementById("logout-btn");
   
    // When clicking the add athlete button
    const addAthBtn = document.querySelector(".add-ath");
    const addModal = document.getElementById("add-AthModal");
    const quitAdd = document.getElementById("quitAdd");
    const addForm = document.getElementById("AddAth-form");

    if (addAthBtn && addModal){
        addAthBtn.addEventListener("click", function (event){
            event.preventDefault();
            addModal.classList.remove("hidden");
        });
    }

    if (quitAdd){
        quitAdd.addEventListener("click", function(){
            addModal.classList.add("hidden");
        });
    }

    addModal.addEventListener("click", function(event){
        if (event.target === addModal){
            addModal.classList.add("hidden");
        }
    });

    // This method will prevent multiple submissions of the forms
    addForm.addEventListener("submit", function(e) {
        if (this.dataset.submitted) {
            e.preventDefault();
            return false;
        }
        this.dataset.submitted = true;
    });

    // This is for selecting the athlete
    /*
        THis method, I use some help from the chatbot for better
        optimization of the code

        When clicked selected button, the athlete card will be able to
        select. Clicked cancel to cancel the selection
    */
    const selectBtn = document.querySelector(".select-ath");
    const cancelBtn = document.querySelector(".cancel");
    const deleteBtn = document.querySelector(".delete-select");
    const athleteCards = document.querySelectorAll(".athlete-card");

    let selectionMode = false;
    let selectedAthletes = new Set();

    selectBtn.addEventListener("click", function () {
        selectionMode = true;
        selectBtn.classList.add("hidden");
        cancelBtn.classList.remove("hidden");
        deleteBtn.classList.remove("hidden");
        selectBtn.disabled = true;

        athleteCards.forEach(card => {
            card.classList.add("selectable");
        });
    });

    cancelBtn.addEventListener("click", function () {
        selectionMode = false;
        selectedAthletes.clear();
        athleteCards.forEach(card => card.classList.remove("selected", "selectable"));
        cancelBtn.classList.add("hidden");
        deleteBtn.classList.add("hidden");
        selectBtn.classList.remove("hidden");
        selectBtn.disabled = false;
    });

    athleteCards.forEach(card => {
        card.addEventListener("click", function () {
            if (!selectionMode){
                 return;
            }

            const athleteId = card.dataset.id;
            if (!athleteId) {
                return;
            }

            if (selectedAthletes.has(athleteId)) {
                selectedAthletes.delete(athleteId);
                card.classList.remove("selected");
            } 
            else {
                selectedAthletes.add(athleteId);
                card.classList.add("selected");
            }
        });
    });

    // Delete selected athletes
    deleteBtn.addEventListener("click", function () {
        if (selectedAthletes.size === 0) {
            alert("Please select athlete to delete (Nothing selected)");
            return;
        }

        if (!confirm("Are you sure you want to delete all of these?")){
            return;
        }

        const csrfToken = getCookie("csrftoken");

        const form = document.createElement("form");
        form.method = "POST";
        form.action = "";  
        form.style.display = "none";

        const csrfInput = document.createElement("input");
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        selectedAthletes.forEach(id => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "delete_ids";  
            input.value = id;
            form.appendChild(input);
        });

        document.body.appendChild(form);
        form.submit();
    });

    /// Use images
    if (userImg) {
        userImg.onclick = function (e) {
            e.stopPropagation();
            userMenu.style.display = userMenu.style.display === "block" ? "none" : "block";
        };

        document.onclick = function () {
            userMenu.style.display = "none";
        };
    }

    if (logoutBtn) {
        logoutBtn.onclick = function () {
            fetch("/logout/", {  
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "logged out") {
                    location.reload();
                }
            });
        };
    }

    /*
        Search and filter. This works with django 
        (only for the gender filter)
    */
    const params = new URLSearchParams(window.location.search);
    const gender = params.get("gender");
    if (gender) {
        const genderFilter = document.getElementById("gender-filter");
        if (genderFilter) {
            genderFilter.value = gender;
        }
    }

    // The zoom card function
    // When I hover and clicked the user icon inside the athlete card, 
    // the program will zoom the card (clone the card and display it again)
    document.body.addEventListener("click", function(event) {
        if ( // when these condition met, the zoom will not activate
            event.target.matches(".hover-images img") && 
            !event.target.closest(".delete-athlete-form") &&
            !event.target.classList.contains("edit-btn")
        ) {
            event.stopPropagation();

            let card = event.target.closest(".athlete-card");

            let overlay = document.createElement("div");
            overlay.className = "zoom-overlay";
            document.body.appendChild(overlay);

            let clonedCard = card.cloneNode(true);
            clonedCard.classList.add("zoomed-card");

            let closeBtn = document.createElement("button");
            closeBtn.className = "zoom-close-btn";
            closeBtn.innerHTML = "X";
            clonedCard.appendChild(closeBtn);

            document.body.appendChild(clonedCard);

            function closeZoom() {
                clonedCard.remove();
                overlay.remove();
            }

            closeBtn.addEventListener("click", closeZoom);
            overlay.addEventListener("click", closeZoom);
        }
    });

    // Editing form athletes
    const editBtns = document.querySelectorAll(".edit-btn");
    const modal = document.getElementById("editFormModal");
    const form = document.getElementById("athleteEditForm");

    editBtns.forEach(btn => {
        /*
            This method will get the data from the database
            using this.dataset.firstname (this is example to get the firstname From Db)
            through the id of the input fields

            After clicked the form submission it will save the data to db (new edit data)
        */
        btn.addEventListener("click", function (event) {
            document.getElementById("athlete_id").value = this.dataset.id;
            document.getElementById("firstName").value = this.dataset.firstname;
            document.getElementById("lastName").value = this.dataset.lastname;
            document.getElementById("gender").value = this.dataset.gender;

            modal.classList.remove("hidden"); 
        });
    });

    window.closeEditForm = function () {
        modal.classList.add("hidden"); 
    }

    modal.addEventListener("click", function(event){
        if(event.target === modal){
            closeEditForm();
        }
    });

    // athletes deletion handle (when hover and clicked deleted bin btn)
    // This will delete the athlete, but there will be alert before you delete asking yes or no
    const deleteForms = document.querySelectorAll(".delete-athlete-form");
    deleteForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            const confirmDelete = confirm("Are you sure you want to delete this athlete?");
            if (!confirmDelete) {
                event.preventDefault(); 
                return;
            }

            const athleteId = form.querySelector("input[name='athlete_id']").value;
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "delete_ids";
            input.value = athleteId;
            form.appendChild(input);
        });
    });
});


/*
This function, I really dont know how to use sessions and cookies
in JS, so I ask chatbot for the solution since I struggles with
this stuff for a while
*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
