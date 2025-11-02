document.addEventListener("DOMContentLoaded", function () {
    let thumbnails = document.querySelectorAll(".thumbnail");
    let mainImage = document.getElementById("mainImage");

    for (let i = 0; i < thumbnails.length; i++) {
        thumbnails[i].addEventListener("click", function () {
            let newSrc = this.getAttribute("src");

            mainImage.style.opacity = "0";

            setTimeout(function () {
                mainImage.src = newSrc;
                mainImage.style.opacity = "1";
            }, 200);

            for (let j = 0; j < thumbnails.length; j++) {
                thumbnails[j].classList.remove("active");
            }

            this.classList.add("active");
        });
    }
});
