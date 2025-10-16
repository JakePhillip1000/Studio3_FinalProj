document.addEventListener("DOMContentLoaded", function() {
    const addBtn = document.querySelector(".add-team-btn");
    const popupOverlay = document.getElementById("popupOverlay");
    const quitBtn = document.querySelector(".quit-btn");
    const gold = document.getElementById("gold");
    const silver = document.getElementById("silver");
    const bronze = document.getElementById("bronze");
    const total = document.getElementById("total");
    const teamName = document.getElementById("team-name");
    const teamId = document.getElementById("team-id");

    addBtn.addEventListener("click", function() {
        popupOverlay.style.display = "flex";
    });

    quitBtn.addEventListener("click", function() {
        popupOverlay.style.display = "none";
        clearForm();
    });

    popupOverlay.addEventListener("click", function(e) {
        if (e.target === popupOverlay) {
            popupOverlay.style.display = "none";
            clearForm();
        }
    });

    function updateTotal() {
        const totalValue = (Number(gold.value) || 0) + (Number(silver.value) || 0) + (Number(bronze.value) || 0);
        total.value = totalValue;
    }

    gold.addEventListener("input", updateTotal);
    silver.addEventListener("input", updateTotal);
    bronze.addEventListener("input", updateTotal);

    function clearForm() {
        teamName.value = "";
        gold.value = 0;
        silver.value = 0;
        bronze.value = 0;
        total.value = 0;
        teamId.value = "";
    }
});
