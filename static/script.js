document.addEventListener('DOMContentLoaded', function() {
    const confirmButton = document.querySelector('#vacation-form button[type="submit"]');
    const vacationForm = document.getElementById('vacation-form');
    const modal = document.getElementById('confirmation-dialog');
    const confirmYesButton = document.getElementById('confirm-yes');  // Updated to use id for the "Yes" button
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

    function confirmSelection(event) {
        event.preventDefault(); // Prevent the default form submission
        const checkboxes = document.querySelectorAll('#vacation-options input[type="checkbox"]');
        const selectedWeeks = Array.from(checkboxes)
                            .filter(checkbox => checkbox.checked)
                            .map(checkbox => checkbox.name);

        if (selectedWeeks.length === 0) {
            alert('Please select at least one vacation week.');
        } else if (modal) {
            modal.style.display = "block"; // Display the confirmation dialog
        }
    }

    vacationForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        updateEmployeeTable();
    });

    function updateEmployeeTable() {
        fetch('/employee_information')
            .then(response => response.text())
            .then(data => {
                document.querySelector('.container').innerHTML = data;
            })
            .catch(error => console.error('Error updating employee table:', error));
    }
});

function submitSelection() {
    closeModal(); // Close the modal when "Yes" button is clicked

    window.location.href = '/employee_information';

    // Get the form data
    const formData = new FormData(document.getElementById('vacation-form'));

    // Make an AJAX request to submit the form data
    fetch('/process_vacation_selection', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Check the Content-Type of the response
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json(); // Parse the response as JSON
            } else {
                return response.text(); // Return the response as text
            }
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
