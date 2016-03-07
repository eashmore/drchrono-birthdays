function checkForEmailUpdate() {
  var $patientList = $('#patient-list');
  $patientList.on('change', 'input', prepareForSave);

  var $allUserButton = $('#email-all-button');
  $allUserButton.on('click', updateAllPatients);
}

function updateAllPatients(e) {
  e.preventDefault();
  var patients = $('.patient');
  saveChanges(patients);
}

function prepareForSave(e) {
  var checkbox = e.currentTarget;
  var patientNode = checkbox.parentNode.parentNode;
  if (patientNode.classList.contains('changed')) {
    patientNode.classList.remove('changed');
  } else {
    patientNode.classList.add('changed');
  }
  activateSaveButton();
}

function activateSaveButton() {
  var $button = $('#save-send-changes');
  if ($button.attr('disabled')) {
    $button.removeAttr('disabled');
    $button.addClass('enabled-button');
    $button.on('click', getChanges);
  }
}

function getChanges(e) {
  e.preventDefault();
  var button = e.currentTarget;
  button.textContent = 'Saving changes...';
  button.disabled = true;
  var $changedPatients = $('#patient-list').find('.changed');
  saveChanges($changedPatients);
}

function saveChanges($patientsList) {
  $('#saving-wall').removeClass('display-none');
  var requests = [];
  for (var i = 0; i < $patientsList.length; i++) {
    requests.push(buildPutRequest($patientsList[i]));
  }

  $.when.apply($, requests).done(function() {
    window.location.reload();
  });
}

function buildPutRequest(patient) {
  var checkbox = patient.querySelector('input');
  var bool = true;
  if (patient.classList.contains('changed') && !checkbox.checked) {
    bool = false;
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
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                                cookie.substring(name.length + 1)
                              );
                break;
            }
        }
    }
    return cookieValue;
}

(function() {
  checkForEmailUpdate();
})();
