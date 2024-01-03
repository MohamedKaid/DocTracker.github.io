document.addEventListener('DOMContentLoaded', function() {
    // Buttons
    const changeEmailButton = document.querySelector('.change-email');
    const changePasswordButton = document.querySelector('.change-password');
    const updateForm = document.querySelector('.update-form');
  
    // Button event listeners
    changeEmailButton.addEventListener('click', function() {
      showForm('New Email', 'email');
    });
    changePasswordButton.addEventListener('click', function() {
      showForm('New Password', 'password');
    });
  
    // Show form based on value being updated
    function showForm(title, newValue) {
      // Set input attributes
      const input = document.getElementById('new-value');
      input.value = '';
      input.name = newValue;
      input.type = `${newValue}`;

      // Restrict input if password
      if (newValue == 'password'){
        input.pattern = '[0-9]*';
        input.maxLength = '4';
      }

      // Set label attributes
      document.querySelector('label[for=new-value]').textContent = `${title}:`;
      
      // Show form div
      updateForm.classList.remove('hidden');
    }
  
    // Execute update
    const settingsForm = document.querySelector('.settings-form');
    settingsForm.addEventListener('submit', function(event) {
        // Prevent form submission
        event.preventDefault();

        // Clear error message
        $('#error-message').text('');
        
        var formData = new FormData(this);
        formData.append('newValue', document.getElementById('new-value').name);

        $.ajax({
          url: '/account/update-user-info',
          method: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function() {
              // Redirect on successful login
              window.location.href = '/account/settings';
          },
          error: function(xhr, status, error) {
              // Show incorrect credentials message
              if(xhr.status === 400) {
                  var errorMessage = xhr.responseJSON.error ? xhr.responseJSON.error : 'Incorrect email or pin';
                  $('#error-message').text(errorMessage);
              }
          }
        });
    });
});

  
  