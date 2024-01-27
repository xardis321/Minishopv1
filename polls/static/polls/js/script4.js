document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    const addItemForm = document.getElementById("addItemForm");
  
    // Add an event listener to the form's submit button
    addItemForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(addItemForm);
        
        try {
            const response = await axios.post('/add_item/', formData);

            if (response.data.redirect_url) {
                // Redirect to the specified URL
                window.location.href = response.data.redirect_url;
            } else {
                console.log("Item added successfully!");
            }
        } catch (error) {
            console.error("An error occurred:", error);
        }
    });
});
