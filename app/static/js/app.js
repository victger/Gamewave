$(document).ready(function() {

    // Gestionnaire pour afficher le champ de recherche quand une colonne est cliquée
    $('.searchable-column').on('click', function() {
        const searchField = $(this).data('search');

        // Cache tous les champs de recherche
        $('.search-group').hide();

        // Affiche le champ correspondant en fonction de la colonne cliquée
        switch (searchField) {
            case 'game':
                $('#game-search-container').show();
                break;
            case 'video-title':
                $('#video-title-search-container').show();
                break;
            case 'channel':
                $('#channel-search-container').show();
                break;
            case 'date':
                $('#date-search-container').show();
                break;
            case 'tags':
                $('#tags-search-container').show();
                break;
        }
    });

    // Auto-complétion pour les champs de recherche
    setupAutocomplete('#game-search', '#game-suggestions', 'Game');
    setupAutocomplete('#video-title-search', '#video-title-suggestions', 'Video title');
    setupAutocomplete('#channel-search', '#channel-suggestions', 'Channel');
    setupAutocomplete('#tags-search', '#tags-suggestions', 'Tags');

    function setupAutocomplete(inputSelector, suggestionSelector, field) {
        let debounce;
        $(inputSelector).on('input', function () {
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                getAutoComplete($(inputSelector).val().trim(), field, suggestionSelector);
            }, 300);
        });

        // Lorsqu'une suggestion est cliquée, on la place dans la boîte de recherche
        $(document).on('click', suggestionSelector + ' li', function() {
            $(inputSelector).val($(this).text());
            $(suggestionSelector).empty().hide(); // Cache le menu après sélection
        });
    }

    function getAutoComplete(query, field, suggestionSelector) {
        if (query === "") {
            $(suggestionSelector).empty().hide(); // Cache le menu si le champ est vide
            return;
        }

        fetch(`/autocompletion?field=${field}&q=${encodeURIComponent(query)}`)
            .then((resp) => resp.json())
            .then((data) => {
                $(suggestionSelector).empty().show(); // Vide et affiche le menu des suggestions
                for (let i = 0; i < data.length; i++) {
                    $(suggestionSelector).append(`<li>${data[i]}</li>`);
                }
            });
    }
});

function search_date() {
    let specific_date = document.getElementById("datepicker").value;
    if (specific_date) {
        window.location.href = `/search_date?date=${encodeURIComponent(specific_date)}`;
    } else {
        alert("Please select a date first.");
    }
}

function sortTable(order) {
    var table = document.getElementById('results-table');
    var rows = Array.from(table.getElementsByTagName('tr'));
    
    rows.sort(function(a, b) {
        var viewsA = parseInt(a.getElementsByTagName('td')[3].textContent);
        var viewsB = parseInt(b.getElementsByTagName('td')[3].textContent);
        
        if (order === 'asc') {
            return viewsA - viewsB;
        } else {
            return viewsB - viewsA;
        }
    });

    rows.forEach(function(row) {
        table.appendChild(row);
    });
}