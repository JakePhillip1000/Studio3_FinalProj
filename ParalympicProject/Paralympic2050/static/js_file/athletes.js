window.addEventListener("DOMContentLoaded", initUserMenu);

function initUserMenu() {
    const userImg = document.getElementById("user-img");
    const userMenu = document.getElementById("user-menu");
    const logoutBtn = document.getElementById("logout-btn");

    userImg.onclick = function (e) {
        e.stopPropagation();
        userMenu.style.display = userMenu.style.display === "block" ? "none" : "block";
    };

    document.onclick = function() {
        userMenu.style.display = "none";
    };

    logoutBtn.onclick = function() {
        fetch("/logout/", {  
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            },
        }).then(response => response.json()).then(data => {
              if(data.status === "logged out") {
                  location.reload(); 
              }
          });
    };
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
    const deleteForms = document.querySelectorAll(".delete-athlete-form");

    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const confirmDelete = confirm("Are you sure you want to delete this athlete?");
            if (!confirmDelete) {
                e.preventDefault(); 
            }
        });
    });