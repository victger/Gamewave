$(function() {
    $("#datepicker").datepicker({
        numberOfMonths: 2,
        dateFormat: 'yy-mm-dd',  // Format de la date
        onSelect: function(selectedDate) {
            var datepickerData = $(this).data().datepicker;

            if (!datepickerData.first) {
                datepickerData.inline = true;
                datepickerData.first = selectedDate;
            } else {
                if (selectedDate > datepickerData.first) {
                    $(this).val(datepickerData.first + " - " + selectedDate);
                } else {
                    $(this).val(selectedDate + " - " + datepickerData.first);
                }
                datepickerData.inline = false;
            }
        },
        onClose: function() {
            var datepickerData = $(this).data().datepicker;
            delete datepickerData.first;
            datepickerData.inline = false;
        }
    });
});

// Fonction pour rechercher par date
function search_date() {
    let specific_date = document.getElementById("datepicker").value;
    if (specific_date) {
        window.location.href = `http://localhost:5000/search_date?date=${encodeURIComponent(specific_date)}`;
    } else {
        alert("Please select a date first.");
    }
}