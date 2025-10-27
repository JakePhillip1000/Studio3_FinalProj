document.addEventListener("DOMContentLoaded", function(){
    // For this one, When click the filter button inside the page, the form will appear
    // Also when clicked quit, the form will close
    const modal = document.getElementById("filterModal");
    const filterBtn = document.querySelector(".filter-btn");
    const quitBtn = document.querySelector(".quit-btn");
    const filterForm = document.getElementById("filterForm");

    filterBtn.addEventListener("click", function(){
        modal.style.display = "block";
    });

    quitBtn.addEventListener("click", function(){
        modal.style.display = "none";
    });

    window.addEventListener("click", function(event){
        if (event.target === modal){
            modal.style.display = "none";
        }
    });

    /*
        When submitting the form, the form will be converted into URL parameters
        The page reloads with new URL containing filters and the django view will read
        the URL parameters and filtering the event
    */
    filterForm.addEventListener("submit", function(event){
        event.preventDefault();
        
        const formData =  new FormData(filterForm);
        const params = new URLSearchParams();

        for (let [key, value] of formData.entries()){
            if (value.trim() !== "") {
                params.append(key, value.trim());
            }  
        }

        const currentUrl = window.location.pathname;
        window.location.href = currentUrl + "?" + params.toString();
    });

    function FilterFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        
        urlParams.forEach(function(value, key) {
              const input = filterForm.querySelector('[name="' + key + '"]');
            if (input) {
                if (input.type === "radio") {
                    const checkRadio = filterForm.querySelector('[name="' + key + '"][value="' + value + '"]');
                    if (checkRadio) {
                        checkRadio.checked = true;
                    }
                } 
                else {
                    input.value = value;
                }
            }
        });
    }

    FilterFromURL();
});