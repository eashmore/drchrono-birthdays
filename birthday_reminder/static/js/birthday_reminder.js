// Add listeners for patient updates
function listenForPatientUpdate() {
  var $allPatientsButton = $('#email-all-button');
  $allPatientsButton.on('click', toggleAllPatients);

  var $noPatientsButton = $('#email-none-button');
  $noPatientsButton.on('click', toggleAllPatients);

  var $patientList = $('#patient-list');
  $patientList.on('change', 'input', markUserForUpdate);
}

// Update all patients
function toggleAllPatients(e) {
  e.preventDefault();
  var sendAll = true;
  if (e.currentTarget.id === 'email-none-button') {
    sendAll = false;
  }

  var patients = $('.patient');
  saveChanges(patients, sendAll);
}

function markUserForUpdate(e) {
  var checkbox = e.currentTarget;
  var patientEl = checkbox.parentNode.parentNode;
  if (patientEl.classList.contains('changed')) {
    patientEl.classList.remove('changed');
  } else {
    patientEl.classList.add('changed');
  }
  activateSaveButton();
}

function activateSaveButton() {
  var $saveButton = $('#save-send-changes');
  if ($saveButton.attr('disabled')) {
    $saveButton.removeAttr('disabled');
    $saveButton.addClass('enabled-button');
    $saveButton.on('click', getMarkedPatients);
  }
}

function getMarkedPatients(e) {
  e.preventDefault();
  var saveButton = e.currentTarget;
  saveButton.disabled = true;
  var $changedPatients = $('#patient-list').find('.changed');
  saveChanges($changedPatients);
}

function saveChanges($patientsList, boolean) {
  $('#save-guard').removeClass('display-none');
  var requests = [];
  for (var i = 0; i < $patientsList.length; i++) {
    if (boolean === undefined) {
      boolean = isChecked($patientsList[i]);
    }

    requests.push(buildPutRequest($patientsList[i], boolean));
    updatePatientEl($patientsList[i], boolean);
  }
  sendRequests(requests);
}

// Sends all ajax requests at once and runs callback after all are complete
function sendRequests(requests) {
  $.when.apply($, requests).done(function() {
    $('#save-guard').addClass('display-none');
    successSave();
  });
}

// Check whether or not a marked patient should be sent an email after update
function isChecked(patient) {
  var checkbox = patient.querySelector('input');
  if (checkbox.checked) {
    return true;
  }

  return false;
}

// Updates patient DOM element to reflect changes from update
function updatePatientEl(patient, bool) {
  var checkbox = patient.querySelector('input');
  if (bool) {
    checkbox.checked = true;
  } else {
    checkbox.checked = false;
  }

  patient.classList.remove('changed');
}

function buildPutRequest(patient, bool) {
  var csrftoken = getCookie('csrftoken');
  return $.ajax({
    url: 'api/patient/' + patient.getAttribute('id') + '/',
    type: 'put',
    data: {'email_bool': bool},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
}

// Add listener for doctor email updates
function listenForEmailUpdate() {
  var $button = $('#email-submit');
  $button.on('click', saveEmail);
}

function saveEmail(e) {
  e.preventDefault();
  var button = e.currentTarget;
  button.disabled = true;
  var $form = $(e.currentTarget.parentElement);
  var data = $form.serialize();

  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/api/doctor/' + $form.data('user') +'/',
    type: 'put',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function() {
      button.disabled = false;
      successSave();
    }
  });
}

// Displays message on successful save
function successSave() {
  var saveSuccess = $('#save-success');
  saveSuccess.removeClass('display-none');
  setTimeout(function() {
    saveSuccess.addClass('display-none');
  }, 1500);
}

// From Django docs https://docs.djangoproject.com/en/1.9/ref/csrf/
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
  listenForPatientUpdate();
  listenForEmailUpdate();
})();
