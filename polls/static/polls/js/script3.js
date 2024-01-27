document.addEventListener("DOMContentLoaded", function () {
    const invoiceTable = document.getElementById("invoiceTable");
    const purchaseOrderTable = document.getElementById("purchaseOrderTable");
    const searchField = document.getElementById("searchField");

    // Sort the tables based on the column header clicked
    const sortTable = (table, column) => {
        const rows = Array.from(table.querySelectorAll("tbody tr"));

        rows.sort((a, b) => {
            const cellA = a.querySelector(`td:nth-child(${column})`).innerText;
            const cellB = b.querySelector(`td:nth-child(${column})`).innerText;
            return cellA.localeCompare(cellB, "en", { numeric: true });
        });

        rows.forEach((row) => table.querySelector("tbody").appendChild(row));
    };

    // Attach click event listener to each column header in the tables
    document.querySelectorAll(".invoice-table th, .purchase-order-table th").forEach((th, index) => {
        th.addEventListener("click", () => {
            const table = th.closest("table");
            sortTable(table, index + 1);
        });
    });

    // Filter the tables based on the search input
    searchField.addEventListener("input", () => {
        const searchValue = searchField.value.toLowerCase();
        const invoiceRows = Array.from(invoiceTable.querySelectorAll("tbody tr"));
        const purchaseOrderRows = Array.from(purchaseOrderTable.querySelectorAll("tbody tr"));

        invoiceRows.forEach((row) => {
            const customer = row.querySelector("td:first-child").innerText.toLowerCase();
            const date = row.querySelector("td:nth-child(2)").innerText.toLowerCase();
            row.style.display = (customer.includes(searchValue) || date.includes(searchValue)) ? "" : "none";
        });

        purchaseOrderRows.forEach((row) => {
            const supplier = row.querySelector("td:first-child").innerText.toLowerCase();
            const date = row.querySelector("td:nth-child(2)").innerText.toLowerCase();
            row.style.display = (supplier.includes(searchValue) || date.includes(searchValue)) ? "" : "none";
        });
    });

    // Handle checkbox changes for marking invoices as completed
    document.querySelectorAll(".invoice-complete").forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            const invoiceId = checkbox.dataset.invoiceId;
            const isCompleted = checkbox.checked;

            // Send the data to the server using fetch API
            fetch(`/api/mark_invoice_complete/${invoiceId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"), 
                },
                body: JSON.stringify({ is_completed: isCompleted }),
            })
                .then((response) => {
                    if (response.ok) {
                        console.log("Invoice marked as completed.");
                    } else {
                        console.error("Error marking invoice as completed.");
                    }
                })
                .catch((error) => {
                    console.error("Error marking invoice as completed:", error);
                });
        });
    });

    // Handle checkbox changes for marking purchase orders as completed
    document.querySelectorAll(".purchase-order-complete").forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            const purchaseOrderId = checkbox.dataset.purchaseId;
            const isCompleted = checkbox.checked;

            // Send the data to the server using fetch API
            fetch(`/api/mark_purchase_order_complete/${purchaseOrderId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"), 
                },
                body: JSON.stringify({ is_completed: isCompleted }),
            })
                .then((response) => {
                    if (response.ok) {
                        console.log("Purchase order marked as completed.");
                    } else {
                        console.error("Error marking purchase order as completed.");
                    }
                })
                .catch((error) => {
                    console.error("Error marking purchase order as completed:", error);
                });
        });
    });

    async function refreshView() {
        const response = await fetch('/income-and-expenditure/');
        const content = await response.text();
        const parser = new DOMParser();
        const newDoc = parser.parseFromString(content, 'text/html');
        const newContent = newDoc.querySelector('.content');
        document.querySelector('.content').replaceWith(newContent);
    }

    // Funkcja do aktualizacji statusu faktury/zamówienia
    async function updateStatus(statusElement) {
        const status = statusElement.dataset.status;
        const itemId = statusElement.dataset.invoiceId || statusElement.dataset.purchaseId;
        const isCompleted = statusElement.checked;

        const csrfToken = getCSRFToken();
        await fetch(`/${status}-status/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ is_completed: isCompleted }),
        });

        await refreshView();
    }

    // Nasłuchiwanie na zmiany w statusie
    const statusCheckboxes = document.querySelectorAll('.invoice-complete, .purchase-order-complete');
    statusCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => updateStatus(checkbox));
    });

    // Fake API call function for demonstration purposes
    function fakeAPICall(endpoint, data) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({ status: "success", data });
            }, 500);
        });
    }

    // You need to implement this function to get the CSRF token from the cookie
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
    }
});
