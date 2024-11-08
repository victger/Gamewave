$(function() {
    $("#datepicker").datepicker({
        numberOfMonths: 2,
        dateFormat: 'yy-mm-dd',  // Spécifie le format de la date
        onSelect: function(selectedDate) {
            if (!$(this).data().datepicker.first) {
                $(this).data().datepicker.inline = true;
                $(this).data().datepicker.first = selectedDate;
            } else {
                if (selectedDate > $(this).data().datepicker.first) {
                    $(this).val($(this).data().datepicker.first + " - " + selectedDate);
                } else {
                    $(this).val(selectedDate + " - " + $(this).data().datepicker.first);
                }
                $(this).data().datepicker.inline = false;
            }
        },
        onClose: function() {
            delete $(this).data().datepicker.first;
            $(this).data().datepicker.inline = false;
        }
    });
});

function search_date() {
    let specific_date = document.getElementById("datepicker").value;
    window.location.href = `http://localhost:5000/search_date?date=${encodeURIComponent(specific_date)}`;
}