function checkForEmailUpdate() {
  var $patientList = $('#patient-list');
  $patientList.on('change', 'input', prepareForSave);

  var $allPatientsButton = $('#email-all-button');
  $allPatientsButton.on('click', updateAllPatients);
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
    type: 'put',
    data: {'email_bool': bool},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
}

function checkForEmailSave() {
  var $button = $('#email-submit');
  $button.on('click', saveEmail);
}

function saveEmail(e) {
  e.preventDefault();
  var button = e.currentTarget;
  button.disabled = true;
  var $form = $(e.currentTarget.parentElement);
  var data = $form.serialize();
  var user_id = $form.data('user');

  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/api/doctor/' + user_id +'/',
    type: 'put',
    data: data,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function() {
      button.disabled = false;
      var saveSuccess = $('#save-success');
      saveSuccess.removeClass('display-none');
      setTimeout(function() {
        saveSuccess.addClass('display-none');
      }, 1500);
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
  checkForEmailSave();
})();
