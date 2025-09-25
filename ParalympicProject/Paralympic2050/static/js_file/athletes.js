window.addEventListener("DOMContentLoaded", initUserMenu);

function initUserMenu() {
    const userImg = document.getElementById("user-img");
    const userMenu = document.getElementById("user-menu");
    const logoutBtn = document.getElementById("logout-btn");
    const loginBtn = document.getElementById("login-btn");

    userImg.onclick = function (e) {
        e.stopPropagation();
        userMenu.style.display = userMenu.style.display === "block" ? "none" : "block";
    };

    document.onclick = function() {
        userMenu.style.display = "none";
    };

    if (logoutBtn) {
        logoutBtn.onclick = function() {
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
}

// Searching features in JS for selected gender 
const search = new URLSearchParams(window.location.search);
const gender = params.get("gender");
if (gender) {
    document.getElementById("gender-filter").value = gender;
}


// Zoom the athelete card when I cliked the user_image
let zoom_athletes = document.querySelectorAll(".hover-images img");

for (let i = 0; i < zoom_athletes.length; i++) {
    zoom_athletes[i].addEventListener("click", function(event) {
        
        if (event.target.closest(".delete-athlete-form")){
            return; 
        }

        event.stopPropagation();

        let card = this.closest(".athlete-card");

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
    });
}


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


// athletes deletion handle
// This will delete the athlete, but there will be alert before you delete asking yes or no
const deleteForms = document.querySelectorAll(".delete-athlete-form");

deleteForms.forEach(form => {
    form.addEventListener("submit", function(event) {
        const confirmDelete = confirm("Are you sure you want to delete this athlete?");
        if (!confirmDelete) {
            event.preventDefault(); 
        }
    });
});