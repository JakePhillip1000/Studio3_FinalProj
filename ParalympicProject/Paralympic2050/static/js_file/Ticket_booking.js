document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("filterModal");
    const filterBtn = document.querySelector(".filter-btn");
    const quitBtn = document.querySelector(".quit-btn");
    const filterForm = document.getElementById("filterForm");

    filterBtn.addEventListener("click", function() {
        modal.style.display = "block";
    });

    quitBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    filterForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(filterForm);
        const params = new URLSearchParams();

        for (let [key, value] of formData.entries()) {
            if (value.trim() !== "") {
                params.append(key, value.trim());
            }
        }

        const currentUrl = window.location.pathname;
        window.location.href = currentUrl + "?" + params.toString();
    });

    const ticketModal = document.getElementById("ticketModal");
    const ticketBtns = document.querySelectorAll(".ticket-btn");
    const backBtn = ticketModal.querySelector(".back-btn");
    const bookBtn = ticketModal.querySelector(".book-btn");
    const amountInputs = ticketModal.querySelectorAll('input[type="number"]');
    const ticketForm = document.getElementById("ticketForm");

    function openTicket() {
        ticketModal.style.display = "flex";
    }

    function closeTicketModal() {
        ticketModal.style.display = "none";
        amountInputs.forEach(function(input) {
            input.value = 0;
        });
        updateBookButton();
    }

    ticketBtns.forEach(function(btn) {
        btn.addEventListener("click", function() {
            const eventCard = this.closest('.event-card');
            const eventId = eventCard.dataset.eventId;
            console.log("Setting event ID:", eventId);
            document.getElementById('currentEventId').value = eventId;
            openTicket();
        });
    });

    backBtn.addEventListener("click", closeTicketModal);

    window.addEventListener("click", function(event) {
        if (event.target === ticketModal) {
            closeTicketModal();
        }
    });

    function updateBookButton() {
        let totalAmount = 0;
        amountInputs.forEach(function(input) {
            totalAmount += parseInt(input.value) || 0;
        });

        if (totalAmount > 0) {
            bookBtn.classList.add("active");
        } 
        else {
            bookBtn.classList.remove("active");
        }
    }

    amountInputs.forEach(function(input) {
        input.addEventListener("input", updateBookButton);
    });

    const confirmModal = document.getElementById("confirmationModal");
    const confirmBack = document.getElementById("confirmBackBtn");
    const confirmBtn = document.getElementById("confirmBtn");
    const visaInput = document.getElementById("visaInput");
    const transactionModal = document.getElementById("transactionModal");
    const continueBtn = document.getElementById("continueBtn");

    ticketForm.addEventListener("submit", function(event) {
        event.preventDefault();
    });

    bookBtn.addEventListener("click", function(event) {
        event.preventDefault();
        if (!bookBtn.classList.contains("active")) {
            alert("Please select at least one ticket.");
            return;
        }

        const selectedTickets = getTickets();
        if (selectedTickets.length === 0) {
            alert("Please select at least one ticket.");
            return;
        }

        showConfirmation(selectedTickets);
    });

    function getTickets() {
        const tickets = [];
        amountInputs.forEach(function(input) {
            const quantity = parseInt(input.value) || 0;
            if (quantity > 0) {
                const price = parseFloat(input.dataset.price) || 0;
                
                tickets.push({
                    name: input.name,
                    price: price,
                    quantity: quantity
                });
            }
        });
        return tickets;
    }

    function showConfirmation(tickets) {
        const confirmationDetails = document.getElementById("confirmationDetails");
        confirmationDetails.innerHTML = "";

        let totalAmount = 0;
        tickets.forEach(function(ticket) {
            const row = document.createElement("div");
            row.className = "confirmation-row";

            const subtotal = ticket.price * ticket.quantity;
            totalAmount += subtotal;
            
            // This one will show the display name on the ticket confirmation part
            const displayName = ticket.name.replace(/_/g, " ")
                                           .replace('ticket ', '')
                                           .replace(/([A-Z])/g, ' $1')
                                           .trim();

            row.innerHTML = `
                <span>${displayName}</span>
                <span>${ticket.quantity}</span>
                <span>${ticket.price}$</span>
            `;
            confirmationDetails.appendChild(row);
        });

        document.getElementById("confirmationTotal").textContent = totalAmount + "$";

        confirmModal.style.display = "flex";
        ticketModal.style.display = "none";
        visaInput.value = "";
    }

    confirmBack.addEventListener("click", function() {
        confirmModal.style.display = "none";
        ticketModal.style.display = "flex";
    });

    confirmBtn.addEventListener("click", function(event) {
        event.preventDefault();

        const visa = visaInput.value.trim();
        if (!visa) {
            alert("Enter the Visa car number");
            return;
        }

        if (visa.length !== 16 || !/^\d+$/.test(visa)) {
            alert("Visa card shold have 16 digits");
            return;
        }

        const tickets = getTickets();
        if (tickets.length === 0) {
            alert("Please select one ticket");
            return;
        }

        showTransactionComplete(tickets, visa);
    });

    function showTransactionComplete(tickets, visa) {
        const transactionDetails = document.getElementById("transactionDetails");
        transactionDetails.innerHTML = "";

        let totalAmount = 0;
        tickets.forEach(function(ticket) {
            const row = document.createElement("div");
            row.className = "confirmation-row";

            const subtotal = ticket.price * ticket.quantity;
            totalAmount += subtotal;

            const displayName = ticket.name.replace(/_/g, " ")
                                           .replace('ticket ', '')
                                           .replace(/([A-Z])/g, ' $1')
                                           .trim();

            row.innerHTML = `
                <span>${displayName}</span>
                <span>${ticket.quantity}</span>
                <span>${ticket.price}$</span>
            `;
            transactionDetails.appendChild(row);
        });

        const totalRow = document.createElement("div");
        totalRow.className = "confirmation-row total";
        totalRow.innerHTML = `
            <span><strong>Total</strong></span>
            <span></span>
            <span><strong>${totalAmount}$</strong></span>
        `;
        transactionDetails.appendChild(totalRow);

        confirmModal.style.display = "none";
        transactionModal.style.display = "flex";

        window.pendingTickets = { tickets: tickets, visa: visa };
    }

    continueBtn.addEventListener("click", function() {
        if (window.pendingTickets) {
            submitTicketForm(window.pendingTickets.tickets, window.pendingTickets.visa);
        } 
        else {
            transactionModal.style.display = "none";
            closeTicketModal();
        }
    });

    function submitTicketForm(tickets, visa) {
        console.log("Submitting form with tickets:", tickets); 
        
        amountInputs.forEach(function(input) {
            input.value = 0;
        });
        
        tickets.forEach(function(ticket) {
            const input = ticketForm.querySelector(`[name="${ticket.name}"]`);
            if (input) {
                input.value = ticket.quantity;
                console.log(`Set ${ticket.name} to ${ticket.quantity}`);
            }
        });

        let visaField = ticketForm.querySelector('[name="visa"]');
        if (!visaField) {
            visaField = document.createElement("input");
            visaField.type = "hidden";
            visaField.name = "visa";
            ticketForm.appendChild(visaField);
        }
        visaField.value = visa;
        ticketForm.submit();
    }

    function FilterFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.forEach(function(value, key) {
            const input = filterForm.querySelector('[name="' + key + '"]');
            if (input) {
                if (input.type === "radio") {
                    const checkRadio = filterForm.querySelector('[name="' + key + '"][value="' + value + '"]');
                    if (checkRadio) checkRadio.checked = true;
                } 
                else {
                    input.value = value;
                }
            }
        });
    }

    FilterFromURL();
});