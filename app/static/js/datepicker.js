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
        "autoUpdateInput": false,
    });

    $('#datepicker').on('apply.daterangepicker', function(ev, picker) {
        toggleSearchButton();
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });

    $('#datepicker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
});