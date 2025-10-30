document.addEventListener("DOMContentLoaded", function() {
    const products = [
        {
            img: STATIC_URL + "img/shop_img/MilanoCortina_mascot2.png",
            name: "Milano Cortina 2026 Milo Mascot",
            price: "€30.00",
            isNew: true
        },

        {
            img: STATIC_URL + "img/shop_img/long_sleeve_tshirt.png",
            name: "Paris 2025 Paralympic Back Print Long Sleeve T-shirt",
            price: "€35.00",
            isNew: false
        },
        
        {
            img: STATIC_URL + "img/shop_img/WinterGames_graphics.png",
            name: "Milano Cortina 2026 Paralympic Winter Games Poster by Carolina Altavilla",
            price: "€37.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/ParalympicJacket.png",
            name: "Milano Cortina 2026 Paralympic Salomon Logo Hoodie",
            price: "€55.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Hat1.png",
            name: "Milano Cortina 2026 Paralympics Solomon Logo Cap",
            price: "€35.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/2024Para_color.png",
            name: "Paris 2024 Paralympics Coloured Pin Badge",
            price: "€3.30",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Graphics_Tshirt.png",
            name: "Paris 2024 Paralympics Graphics T-Shirt",
            price: "€28.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/MilanoCortina_mascot1.png",
            name: "Milano Cortina 2026 Paralympics Mascot Mug",
            price: "€13.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Tshirt1.png",
            name: "Paris 2024 Paralympics Fundamental Panel T-shirt",
            price: "€30.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Paralympic_mascot_keying.png",
            name: "Milano Cortina 2026 Paralympic Milo Mascot Keying ",
            price: "€10.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/France_flag.png",
            name: "The Paralympic Team France Flag",
            price: "€4.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Hat3.png",
            name: "Milano Cortina 2026 Paralympics Salomon Logo Beanie",
            price: "€40.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Para1_France.png",
            name: "The Paralympics Team France",
            price: "€6.00",
            isNew: true
        },

        {
            img: STATIC_URL + "img/shop_img/Paralyympic_bear.png",
            name: "The Paralympic Team France Bear",
            price: "€33.00",
            isNew: false
        },

        {
            img: STATIC_URL + "img/shop_img/Graphics_Tshirt2.png",
            name: "Milano Cortina 2026 Paralympic Salomon Logo Graphics Hoodie",
            price: "€55.00",
            isNew: true
        },

        {
            img: STATIC_URL + "img/shop_img/Plush_mascot.png",
            name: "The Paralympic Team France Plush Mascot",
            price: "€22.00",
            isNew: false
        }
    ];

    let container = document.getElementById("shopContainer");
    for (let i = 0; i < products.length; i++){
        let item = products[i];
        let card = document.createElement("div");
        card.className = "product-card";

        if (item.isNew){
            let newLabel = document.createElement("div");
            newLabel.className = "new-label";
            newLabel.textContent = "NEW";
            card.appendChild(newLabel);
        }

        let imgDiv = document.createElement("div");
        imgDiv.className = "product-image";

        let img = document.createElement("img");
        img.src = item.img;
        img.alt = item.name;
        imgDiv.appendChild(img);

        let infoDiv = document.createElement("div");
        infoDiv.className = "product-info";

        let price = document.createElement("p");
        price.className = "product-price";
        price.textContent = item.price;

        let name = document.createElement("p");
        name.className = "product-name";
        name.textContent = item.name;

        let btn = document.createElement("button");
        btn.className = "buy-btn";
        btn.textContent = "Buy Now";

        infoDiv.appendChild(price);
        infoDiv.appendChild(name);
        infoDiv.appendChild(btn);

        card.appendChild(imgDiv);
        card.appendChild(infoDiv);
        container.appendChild(card);
    }
});

