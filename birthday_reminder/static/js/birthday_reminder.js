function checkForEmailUpdate() {
  var $patientList = $('#patient-list');
  $patientList.on('change', 'input', prepareForSave);
}

function prepareForSave(e) {
  var checkbox = e.currentTarget;
  var patientNode = checkbox.parentNode.parentNode;
  if (patientNode.classList.contains('changed')) {
    patientNode.classList.remove('changed');
  } else {
    patientNode.classList.add('changed');
  }
  activeSaveButton();
}

function activeSaveButton() {
  var $button = $('#save-send-changes');
  if ($button.attr('disabled')) {
    $button.removeAttr('disabled');
    $button.addClass('enabled-button');
    $button.on('click', saveChanges);
  }
}

function saveChanges(e) {
  e.preventDefault();
  var button = e.currentTarget;
  button.textContent = 'Saving changes...';
  button.disabled = true;

  var requests = [];
  var $changedPatients = $('#patient-list').find('.changed');
  for (var i = 0; i < $changedPatients.length; i++) {
    requests.push(buildPutRequest($changedPatients[i]));
  }

  $.when.apply($, requests).done(function() {
    window.location.reload();
  });
}

function buildPutRequest(patient) {
  var checkbox = patient.querySelector('input');
  var bool = false;
  if (checkbox.checked) {
    bool = true;
  }
  var csrftoken = getCookie('csrftoken');
  return $.ajax({
    url: 'api/patient/' + patient.getAttribute('id') + '/',
    type: 'PUT',
    data: {'email_bool': bool},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
}

//From Django docs https://docs.djangoproject.com/en/1.9/ref/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

(function() {
  checkForEmailUpdate();
})();
