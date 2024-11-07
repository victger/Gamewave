$(document).ready(function() {

    // Utilise une fonction générale pour gérer les événements de chaque champ de recherche
    setupAutocomplete("#game-search", "#game-suggestions", "Game");
    setupAutocomplete("#video-title-search", "#video-title-suggestions", "Video title");
    setupAutocomplete("#channel-search", "#channel-suggestions", "Channel");

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

        fetch(`http://localhost:5000/search?field=${field}&q=${encodeURIComponent(query)}`)
            .then((resp) => resp.json())
            .then((data) => {
                console.log(data);
                $(suggestionSelector).empty().show(); // Vide et affiche le menu des suggestions
                for (let i = 0; i < data.length; i++) {
                    $(suggestionSelector).append(`<li>${data[i]}</li>`);
                }
            });
    }
});