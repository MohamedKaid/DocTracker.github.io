// First functions to execute
window.onload = onLoad;


/* Event Listeners */

// Live filter search results
const searchInput = document.getElementById("searchInput");
const dataBody = document.getElementById("dataBody");
const rows = dataBody.getElementsByClassName("clickable-row");
const stables = dataBody.getElementsByClassName("sub-table");

searchInput.addEventListener("input", function () {
    const searchQuery = searchInput.value.toLowerCase();

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const stable = stables[i];
        const td = row.getElementsByTagName("td")[0];
        
        if (td) {
            const txtValue = td.textContent || td.innerText;
            if (txtValue.toLowerCase().includes(searchQuery)) {
                row.style.display = "";
                stable.style.display = "";
            } else {
                row.style.display = "none";
                stable.style.display = "none";
            }
        }
    }
});

// Rotate plus icon within button when clicked
const rotateButton = document.getElementById("rotate-button");
let isRotated = false;

rotateButton.addEventListener("click", function() {
    console.log(rotateButton.classList.toString());
    if(isRotated) {
        rotateButton.classList.remove("rotate");
        rotateButton.classList.add("rotate-reverse");             
    } else {
        rotateButton.classList.remove("rotate-reverse");
        rotateButton.classList.add("rotate");
    }
    
    isRotated = !isRotated;
})

// AJAX will prevent the forms with class='form' from being submitted, instead
// passing data and taking response asynchronously so the modal can be displayed
document.querySelectorAll('.form').forEach(function(form) {
    form.addEventListener('submit', function(event) {
        // Prevent form submission
        event.preventDefault();
        
        // Data entered into form
        var formData = new FormData(this);
        
        $.ajax({
            url: '/data/update',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(xhr) {
                responseDriverId = xhr.success;
                window.location.href = '/data/view?driver_id=' + responseDriverId;
            },
            error: function(xhr, status, error) {
                if (xhr.status === 400) {
                    var errorMessage = xhr.responseJSON.error ? xhr.responseJSON.error : 'Your form is invalid.';
                    $('#validationErrorMessage').text(errorMessage);
                    $('#validationErrorModal').modal('show');
                }
            }
        });
    });
});


// /* Functions */

// Functions to be executed on window load
function onLoad() {
    manageTabSize();
    scrollToDriver();
    setMinDate();
    window.onresize = manageTabSize;
}

// Resize tabs based on table width
function manageTabSize() {
    // Get active table
    var driversTableActive = document.getElementById('drivers-tab').classList.contains('active');
    var documentsTableActive = document.getElementById('documents-tab').classList.contains('active');
    var tableWidth;

    // Get width of active table
    if(driversTableActive) {
        tableWidth = document.getElementById('driver-table').offsetWidth;
    } else if (documentsTableActive) {
        tableWidth = document.getElementById('doc-table').offsetWidth;
    } else {
        // Catch no active table
        tableWidth = document.getElementById('searchInput').offsetWidth;
    }

    // Set tab size based on width of active table
    setTabSize(tableWidth);
}

// Set width of tabs to half of table width
function setTabSize(tableWidth) {
    var tabs = document.querySelectorAll('.nav-tabs .nav-item');
        tabs.forEach(function(tab) {
            tab.style.width = (tableWidth / 2) + 'px';
        });
}

// Auto scroll to focus on driver
function scrollToDriver() {
    // Extract the driver_id from the URL after page reload
    const urlParams = new URLSearchParams(window.location.search);
    const driverIdParam = urlParams.get('driver_id');
    const driverId = driverIdParam === 'null' ? null : driverIdParam;

    // Use the retrieved driver_id to focus on their table
    if (driverId) {
        // row of driver previously edited
        const row = $('#row-' + driverId);

        // subsequent buttons
        const settingsButton = row.find('.settings-button');
        const add = row.find('.addDoc');
        const subTable = row.next('.sub-table');

        // show buttons
        subTable.toggleClass('d-none');
        settingsButton.toggleClass('d-none');
        add.toggleClass('d-none');

        // scroll to the specific row
        $('html, body').animate({
            scrollTop: $('#row-' + driverId).offset().top - ($(window).height() / 4)
        }, 'slow');
    }
}

// Set minimum date for expiration date input
function setMinDate() {
    var today = new Date().toISOString().split('T')[0];
    document.getElementsByName("exp_date")[0].setAttribute('min', today);
}


// Show/hide form when plus button clicked
function showDriverForm() {            
    const addDataForm = document.getElementById("add-data-form");

    if(addDataForm.style.display == "none") {
        addDataForm.style.display = "block";
    } else {
        addDataForm.style.display = "none";
    }
}

// Show/hide documents table when row is clicked
$(document).ready(function() {
    $('.clickable-row').on('click', function() {

        if (!$(this).hasClass('disabled-click')) {
            const settingsButton = $(this).find('.settings-button');
            const add = $(this).find('.addDoc');
            const subTable = $(this).next('.sub-table');

            subTable.toggleClass('d-none');
            settingsButton.toggleClass('d-none');
            add.toggleClass('d-none');

            // Scroll to the specific row when opening sub-table
            if (!subTable.hasClass('d-none')) {
                $('html, body').animate({
                scrollTop: $(this).offset().top
                }, 'slow');
            }
        }
        
    })
})

// Show/hide form when plus button clicked
function showDocumenetForm(event) {
    // prevent closing the row immediately
    event.stopPropagation();

    // retrieve the subsequent form and toggle its view
    const row = $(event.target).closest('.clickable-row');
    const subTable = row.next('.sub-table');
    const addDocForm = subTable.find('.add-doc-form');
    
    addDocForm.toggleClass('d-none');
}

// Show/hide settings buttons
function settings(event) {
    event.stopPropagation();

    const row = $(event.target).closest('.clickable-row');

    const deleteButton = row.find('.button.delete');
    const addButton = row.find('.button.addDoc');
    const subTable = row.next('.sub-table');
    const buttons = subTable.find('.button.delete');

    deleteButton.toggleClass('d-none');
    addButton.toggleClass('d-none');

    buttons.toggleClass('d-none');
    row.toggleClass('disabled-click');
    

    console.log("settings clicked!");
}

// Delete driver
function deleteDriver(driver_id) {
    if (confirm('Are you sure you want to delete this driver?')) {
        // Create form element
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/data/delete_driver';

        // Create input elements
        var driverId = document.createElement('input');
        driverId.type = 'hidden';
        driverId.name = 'driver_id';
        driverId.value = driver_id;

        // Add input elements to form
        form.appendChild(driverId);
        // Add form to body and submit
        document.body.appendChild(form);
        form.submit();
    }
}

// Delete document
function deleteDocument(name, date, driver_id) {
    if (confirm('Are you sure you want to delete this document?')) {
        // Create form element
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/data/delete_document';

        // Create input elements
        var docName = document.createElement('input');
        docName.type = 'hidden';
        docName.name = 'document_name';
        docName.value = name;

        var docDate = document.createElement('input');
        docDate.type = 'hidden';
        docDate.name = 'document_date';
        docDate.value = date;

        var driverId = document.createElement('input');
        driverId.type = 'hidden';
        driverId.name = 'driver_id';
        driverId.value = driver_id;

        // Add input elements to form
        form.appendChild(docName);
        form.appendChild(docDate);
        form.appendChild(driverId);
        // Add form to body and submit
        document.body.appendChild(form);
        form.submit();
    }
}