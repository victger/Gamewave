$(function() {
    $('#datepicker').daterangepicker({
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
        },
        "opens": "left",
        "autoUpdateInput": false, // L'entrée ne sera pas mise à jour automatiquement
    });

    $('#datepicker').on('apply.daterangepicker', function(ev, picker) {
        // Mise à jour du champ de saisie avec le format YYYY-MM-DD
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });

    $('#datepicker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val(''); // Vide le champ si annulé
    });
});


function search_date() {
    let specific_date = document.getElementById("datepicker").value;
    if (specific_date) {
        window.location.href = `http://localhost:5000/search_date?date=${encodeURIComponent(specific_date)}`;
    } else {
        alert("Please select a date first.");
    }
}