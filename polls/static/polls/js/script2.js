document.addEventListener('DOMContentLoaded', function () {
  // Function to get CSRF token
  function getCSRFToken() {
    const csrfCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
    if (csrfCookie) {
      return csrfCookie.split('=')[1];
    } else {
      return null;
    }
  }

  // Function to update total amounts for each item
  function updateTotalAmounts() {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
      const quantity = parseInt(row.querySelector('td:nth-child(3)').textContent, 10);
      const unitPrice = parseFloat(row.querySelector('td:nth-child(4)').textContent);
      const totalAmountCell = row.querySelector('.total_amount');
      const totalAmount = quantity * unitPrice;
      totalAmountCell.textContent = totalAmount.toFixed(2);
    });
    updateTotalOrderAmount();
  }

  // Function to handle amount input changes
  function handleAmountInputChange(event, unitPrice) {
    const input = event.target;
    const amount = parseFloat(input.value);

    if (!isNaN(amount)) {
      const itemId = input.dataset.itemId;
      const totalAmountCell = document.querySelector(`[data-item-id="${itemId}"] .total_amount`);
      const totalAmount = amount * unitPrice;
      totalAmountCell.textContent = totalAmount.toFixed(2);
    }

    updateTotalOrderAmount();
  }

  // Function to update total order amount
  function updateTotalOrderAmount() {
    const rows = document.querySelectorAll('tbody tr');
    let totalOrderAmount = 0;

    rows.forEach(row => {
      const amountInput = row.querySelector('.amountInput');
      const amount = parseFloat(amountInput.value);

      if (!isNaN(amount) && amount >= 0) {
        const unitPrice = parseFloat(row.querySelector('td:nth-child(4)').textContent);
        const totalAmount = amount * unitPrice;
        totalOrderAmount += totalAmount;
      }
    });

    const totalAmountField = document.getElementById('total');
    totalAmountField.value = totalOrderAmount.toFixed(2);
  }

  // Function to save purchase order
  function savePurchaseOrder(supplier, date, totalAmount, items) {
    console.log('Saving purchase order...');
    console.log('Supplier:', supplier);
    console.log('Date:', date);
    console.log('Total Amount:', totalAmount);
    console.log('Items:', items);
  
    const postData = {
      supplier: supplier,
      pubDate: date,
      total: totalAmount,
      items: items,
      csrfmiddlewaretoken: getCSRFToken(),  
    };
  
    console.log('Post Data (before sending):', postData);
  
    fetch('/save_supplier_items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify(postData),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(postData => {
        if (postData.error) {
          showError(postData.error);
        } else {
          showSuccess(postData.message);
          window.location.href = '/income-and-expenditure/';
        }
      })
      .catch(error => {
        showError("An error occurred while saving the purchase order. Please try again.");
      });
  }
  
  // Function to add missing items to Inventory (if not already present)
  function add_missing_items_to_inventory(items) {
    for (const item_data of items) {
      const item_id = item_data.item_id;
      const amount = item_data.amount;
  
      if (item_id && amount && amount >= 1) {
        // Check if the item exists in Inventory
        checkItemExistsInInventory(item_id, exists => {
          if (!exists) {
            // If the item doesn't exist, fetch its info from the source (replace this logic with actual source fetching)
            const item_info = get_item_info_from_source(item_id);
            if (item_info) {
              // Create a new Inventory item with the fetched info
              const new_inventory_item = {
                item: item_info.description,
                description: item_info.description,
                quantity: amount,  // Set initial quantity to the ordered amount
                purchasePrice: item_info.purchase_price,
                salePrice: 0.00,
              };
  
              // Save the new item in Inventory
              if (save_inventory_item(new_inventory_item)) {
                console.log('Saved new item in Inventory.');
                console.log('Item id:', item_id, 'Amount:', amount);
              } else {
                console.log('Failed to save item in Inventory.');
              }
            }
          }
        });
      }
    }
  }

  function get_item_info_from_source(item_id) {
    const url = `/get_item_info/?item_id=${item_id}`;
    return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch item info");
        }
        return response.json();
      })
      .catch(error => {
        console.error("Error fetching item info:", error);
        return null;
      });
  }
  
  // Function to check if an item exists in Inventory
  function checkItemExistsInInventory(item_id, callback) {
    fetch(`/item_exists_in_inventory/?item_id=${item_id}`)
      .then(response => response.json())
      .then(data => {
        const exists = data.exists;
        callback(exists);
      })
      .catch(error => {
        console.error('Error checking item existence:', error);
        callback(false);
      });
  }

  // Function to show error messages
  function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.color = 'red';
  }

  // Function to show success messages
  function showSuccess(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.color = 'green';
  }

  // Function to handle save button click and validate data before saving
  function saveSupplierItems() {
    console.log('Save button clicked.');

    const amountInputs = document.querySelectorAll('.amountInput');
    const supplierInput = document.getElementById('supplierInput');
    const invoiceDate = document.getElementById('invoiceDate');
    const totalAmountField = document.getElementById('total');

    const supplier = supplierInput.value.trim();
    const inputDate = invoiceDate.value;
    const totalAmount = parseFloat(totalAmountField.value);

    const dateParts = inputDate.split('-');
    if (dateParts.length !== 3) {
      showError("Please provide a valid date in DD-MM-YYYY format.");
      return;
    }
    const date = `${dateParts[2]}-${dateParts[1].padStart(2, '0')}-${dateParts[0].padStart(2, '0')}`;

    if (!supplier) {
      showError("Please provide a supplier name.");
      return;
    }

    if (!date) {
      showError("Please provide an invoice date.");
      return;
    }

    if (isNaN(totalAmount) || totalAmount <= 0) {
      showError("Please provide a valid total amount.");
      return;
    }

    const items = [];

    amountInputs.forEach(input => {
      const itemId = input.dataset.itemId;
      const amount = parseFloat(input.value);

      if (!isNaN(amount) && amount > 0) {
        items.push({ item_id: itemId, amount: amount });
      }
    });

    if (items.length === 0) {
      showError("Please provide at least one valid item amount greater than 0.");
      return;
    }

    // Add missing items to Inventory before saving
    add_missing_items_to_inventory(items);

    console.log('Supplier:', supplier);
    console.log('Date:', date);
    console.log('Total Amount:', totalAmount);
    console.log('Items:', items);

    savePurchaseOrder(supplier, date, totalAmount, items);
  }

  // Call updateTotalAmounts on page load
  updateTotalAmounts();

  // Declare the variable for amount inputs outside the loop
  let amountInputs = document.querySelectorAll('.amountInput');
  amountInputs.forEach(input => {
    const quantity = parseInt(input.closest('tr').querySelector('td:nth-child(3)').textContent, 10);
    input.addEventListener('input', event => handleAmountInputChange(event, quantity));
  });

  // Calculate total and save supplier items on button click
  const calculateButton = document.getElementById('calculateButton');
  const saveButton = document.getElementById('saveButton');
  calculateButton.addEventListener('click', updateTotalOrderAmount);
  saveButton.addEventListener('click', saveSupplierItems);
});
