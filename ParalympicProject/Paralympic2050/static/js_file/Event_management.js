document.addEventListener("DOMContentLoaded", function () {
    const mapElement = document.getElementById("map");
    let map, marker;

    function initLeafletMap() {
        map = L.map(mapElement).setView([13.736717, 100.523186], 6); // Bangkok
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }).addTo(map);

        map.on("click", function (e) {
            const lat = e.latlng.lat.toFixed(6);
            const lng = e.latlng.lng.toFixed(6);

            if (marker) {
                marker.setLatLng(e.latlng);
            } else {
                marker = L.marker(e.latlng).addTo(map);
            }

            document.getElementById("location-input").value = `${lat}, ${lng}`;
        });
    }

    const addEventBtn = document.querySelector(".add-event-btn");
    const popUp = document.getElementById("popupOverlay");
    const quitBtn = popUp.querySelector(".quit-btn");

    function openPopup() {
        popUp.classList.remove("hidden");
        popUp.style.display = "flex";
        document.body.classList.add("popup-open");

        setTimeout(() => {
            if (!map) initLeafletMap();
        }, 200);
    }

    function closePopup() {
        popUp.classList.add("hidden");
        popUp.style.display = "none";
        document.body.classList.remove("popup-open");
    }

    addEventBtn.addEventListener("click", function () {
        openPopup();
    });

    quitBtn.addEventListener("click", function () {
        closePopup();
    });

    document.querySelectorAll(".delete-event-form").forEach(form => {
        form.addEventListener("submit", function (event) {
            let confirmDelete = confirm("Are you sure to delete this event?");
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    }); 
    
    // This method will make the admin able to edit the event form
    document.querySelectorAll(".edit-event").forEach(function(button) {
        button.addEventListener("click", function() {
            let editEventId = this.dataset.id;

            document.getElementById("event-id").value = editEventId;

            document.getElementById("event-date").value = this.dataset.date;
            document.getElementById("event-time").value = this.dataset.time;
            document.getElementById("event-number").value = this.dataset.number;
            document.getElementById("event-sport").value = this.dataset.sport;
            document.getElementById("event-classification").value = this.dataset.classification;
            document.getElementById("event-phrase").value = this.dataset.phrase;
            document.getElementById("event-status").value = this.dataset.status;
            document.getElementById("location-input").value = this.dataset.location;

            if (this.dataset.gender === "Male") {
                document.getElementById("male").checked = true;
            } 
            else {
                document.getElementById("female").checked = true;
            }

            openPopup();

            if (this.dataset.location && this.dataset.location.includes(",")) {
                const [lat, lng] = this.dataset.location.split(",").map(Number);
                setTimeout(() => {
                    if (!map) initLeafletMap();
                    map.setView([lat, lng], 13);
                    if (marker) {
                        marker.setLatLng([lat, lng]);
                    } 
                    else {
                        marker = L.marker([lat, lng]).addTo(map);
                    }
                }, 300);
            }
        });
    });
});
