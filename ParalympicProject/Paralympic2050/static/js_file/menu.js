window.addEventListener("DOMContentLoaded", function () {
    const userImg = document.getElementById("user-img");
    const userMenu = document.getElementById("user-menu");
    const logoutBtn = document.getElementById("logout-btn");
   
    /// Use images
    if (userImg) {
        userImg.onclick = function (event) {
            event.stopPropagation();
            userMenu.style.display = userMenu.style.display === "block" ? "none" : "block";
        };

        document.onclick = function () {
            userMenu.style.display = "none";
        };
    }
    
    // Logging out from the system
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
});

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

