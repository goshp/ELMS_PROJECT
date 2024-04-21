document.addEventListener('DOMContentLoaded', function() {
    const confirmButton = document.querySelector('#vacation-form button[type="submit"]');
    const vacationForm = document.getElementById('vacation-form');
    const modal = document.getElementById('confirmation-dialog');
    const confirmYesButton = document.getElementById('confirm-yes');
    const closeModalButton = document.querySelector('.close');
 
    if (confirmButton) {
        confirmButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission
            confirmSelection(event);
        });
    }
 
    if (modal && confirmYesButton && closeModalButton) {
        closeModalButton.addEventListener('click', function() {
            modal.style.display = "none";
        });
 
        confirmYesButton.addEventListener('click', function() {
            vacationForm.submit(); // Submit the form on clicking "Yes" in the dialog
        });
    }

    function updateEmployeeTable() {
        fetch('/employee_information')
            .then(response => response.text())
            .then(data => {
                document.querySelector('.container').innerHTML = data;
            })
            .catch(error => console.error('Error updating employee table:', error));
    }

    function updateTableWithData(data) {
        for (const badgeNumber in data) {
            if (data.hasOwnProperty(badgeNumber)) {
                const selectedWeeks = [];
                const remainingWeeks = [];
                for (const week in data[badgeNumber]) {
                    if (data[badgeNumber][week]) {
                        selectedWeeks.push(week);
                    } else {
                        remainingWeeks.push(week);
                    }
                }
                document.getElementById('selected-weeks-' + badgeNumber).innerText = selectedWeeks.join(', ');
                document.getElementById('remaining-weeks-' + badgeNumber).innerText = remainingWeeks.join(', ');
            }
        }
    }
    
 });

 function submitSelection() {
    closeModal(); // Close the modal when "Yes" button is clicked
    // Redirect to the employee information page
    window.location.href = '/employee_information';
    
    const formData = new FormData(vacationForm); // Get the form data
    
    // Make an AJAX request to submit the form data
    fetch('/process_vacation_selection', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            const contentType = response.headers.get('content-type');
            return contentType && contentType.includes('application/json') ? response.json() : response.text();
        } else {
            throw new Error('Failed to submit the form');
        }
    })
    .then(data => {
        if (typeof data === 'object') {
            console.log('Form submitted successfully', data);
            // Handle JSON response data
        } else {
            console.log('Non-JSON response received:', data);
            // Handle non-JSON response
        }

        updateEmployeeTable(); // Update the employee information table after form submission
    })
    .catch(error => {
        console.error('Error submitting the form:', error);
        // Handle any error or display a message to the user
    });
}

 function closeModal() {
    const modal = document.getElementById('confirmation-dialog');
    modal.style.display = "none";  // Close the modal when "No" button is clicked
}
 
 // Move confirmSelection function outside of the DOMContentLoaded event listener
 function confirmSelection(event) {
    event.preventDefault(); // Prevent the default form submission
    const checkboxes = document.querySelectorAll('#vacation-options input[type="checkbox"]');
    const selectedWeeks = Array.from(checkboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.name);
 
    const modal = document.getElementById('confirmation-dialog'); // Define modal here
 
    if (selectedWeeks.length === 0) {
        alert('Please select at least one vacation week.');
    } else if (modal) {
        modal.style.display = "block"; // Display the confirmation dialog
    }
 }