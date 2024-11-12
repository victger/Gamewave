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
        "showDropdowns": true, // Ajoute des sélecteurs pour mois et années
        "autoApply": true,     // Applique directement la sélection
    });

    $('#datepicker').on('apply.daterangepicker', function(ev, picker) {
        toggleSearchButton();
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });

    $('#datepicker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

    // Ajout pour corriger la superposition avec d'autres éléments de l'interface
    $('#datepicker').data('daterangepicker').container.css('z-index', 9999);  // S'assure que le datepicker est toujours au premier plan
});
