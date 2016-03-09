// Add listeners for patient updates
function listenForPatientUpdate() {
  var $updateListButton = $('#update-list-button');
  $updateListButton.on('click', displayLoading);

  var $allPatientsButton = $('#email-all-button');
  $allPatientsButton.on('click', toggleAllPatients);

  var $noPatientsButton = $('#email-none-button');
  $noPatientsButton.on('click', toggleAllPatients);

  var $patientList = $('#patient-list');
  $patientList.on('change', 'input', markUserForUpdate);
}

function displayLoading() {
  $('#save-guard').removeClass('display-none');
  $('#save-guard').addClass('loading-guard');
  $('#loading-screen').removeClass('display-none');
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
  var patientElement = checkbox.parentNode.parentNode;
  if (patientElement.classList.contains('changed')) {
    patientElement.classList.remove('changed');
  } else {
    patientElement.classList.add('changed');
  }
  activateSaveButton();
}

function activateSaveButton() {
  var $saveButton = $('#save-changes-button');
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
  var isCheck = boolean;
  for (var i = 0; i < $patientsList.length; i++) {
    if (boolean === undefined) {
      isCheck = isChecked($patientsList[i]);
    }

    requests.push(buildPutRequest($patientsList[i], isCheck));
    updatePatientElement($patientsList[i], isCheck);
  }
  sendRequests(requests);
}

// Sends all ajax requests at once and runs callback after all are complete
function sendRequests(requests) {
  $.when.apply($, requests).then(function() {
    $('#save-guard').addClass('display-none');
    successSave();
  }, function() {
    $('#save-guard').addClass('display-none');
    errorSave();
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
function updatePatientElement(patient, bool) {
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
    url: 'api/patient/' + patient.dataset.patient + '/',
    type: 'put',
    data: {'email_bool': bool},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
}

// Add listener for doctor email updates
function listenForEmailUpdate() {
  var $button = $('#save-email-button');
  $button.on('click', saveEmail);
}

function saveEmail(e) {
  e.preventDefault();
  var saveButton = e.currentTarget;
  saveButton.disabled = true;
  var $form = $(e.currentTarget.parentElement);
  var data = $form.serialize();

  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/api/doctor/' + $form.data('user-id') +'/',
    type: 'put',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function() {
      saveButton.disabled = false;
      successSave();
    },
    error: function() {
      saveButton.disabled = false;
      errorSave();
    }
  });
}

// Displays message after save
function successSave() {
  var saveSuccess = $('#save-success');
  showSaveResult(saveSuccess);
}

function errorSave() {
  var saveFail = $('#save-fail');
  showSaveResult(saveFail);
}

function showSaveResult(saveStatus) {
  saveStatus.removeClass('display-none');
  setTimeout(function() {
    saveStatus.addClass('display-none');
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
