document.addEventListener("DOMContentLoaded", function () {
    const mapElement = document.getElementById("map");
    let map, marker;

    /*
        This function will browse the map (the map that I use is open street map),
        since google map is a bit difficult to programmed...
    */
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
            } 
            else {
                marker = L.marker(e.latlng).addTo(map);
            }
            // After selecting the map. Input the location
            document.getElementById("location-input").value = `${lat}, ${lng}`;
        });
    }

    const addEventBtn = document.querySelector(".add-event-btn");
    const popUp = document.getElementById("popupOverlay");
    const quitBtn = popUp.querySelector(".quit-btn");

    addEventBtn.addEventListener("click", function () {
        popUp.classList.remove("hidden");
        popUp.style.display = "flex";

        setTimeout(() => {
            if (!map) initLeafletMap();
        }, 200);
    });

    quitBtn.addEventListener("click", function () {
        popUp.classList.add("hidden");
        popUp.style.display = "none";
    });
});
