$(document).ready(function() {
    $('.searchable-column').on('click', function() {
        const searchField = $(this).data('search');
        const searchContainer = $(`#${searchField}-search-container`);

        $('.search-group').not(searchContainer).slideUp(300); 

        searchContainer.stop(true, true).slideToggle(300); 
    });

    setupAutocomplete('#game-search', '#game-suggestions', 'Game');
    setupAutocomplete('#video-title-search', '#video-title-suggestions', 'Video title');
    setupAutocomplete('#channel-search', '#channel-suggestions', 'Channel');
    setupAutocomplete('#tags-search', '#tags-suggestions', 'Tags');

    $('#game-search, #video-title-search, #channel-search, #tags-search, #datepicker').on('input change', toggleSearchButton);

    function setupAutocomplete(inputSelector, suggestionSelector, field) {
        let debounce;
        $(inputSelector).on('input', function () {
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                getAutoComplete($(inputSelector).val().trim(), field, suggestionSelector);
            }, 300);
        });

        $(document).on('click', suggestionSelector + ' li', function() {
            $(inputSelector).val($(this).text());
            $(suggestionSelector).empty().hide();
        });
    }

    function getAutoComplete(query, field, suggestionSelector) {
        if (query === "") {
            $(suggestionSelector).empty().hide();
            return;
        }

        fetch(`/autocompletion?field=${field}&q=${encodeURIComponent(query)}`)
            .then((resp) => resp.json())
            .then((data) => {
                $(suggestionSelector).empty().show();
                for (let i = 0; i < data.length; i++) {
                    $(suggestionSelector).append(`<li>${data[i]}</li>`);
                }
            });
    }
});

let activeQueries = {};

window.onload = function() {
    const params = new URLSearchParams(window.location.search);
    params.forEach((value, key) => {
        activeQueries[key] = value;
    });
    updateActiveQueries();
};

function toggleSearchButton() {
    const game = document.getElementById("game-search").value.trim();
    const videoTitle = document.getElementById("video-title-search").value.trim();
    const channel = document.getElementById("channel-search").value.trim();
    const dateRange = document.getElementById("datepicker").value.trim();
    const tags = document.getElementById("tags-search").value.trim();

    // Vérifier si l'un des champs est rempli
    if (game || videoTitle || channel || dateRange || tags) {
        document.getElementById("search-btn").style.display = "block";  // Afficher le bouton
    } else {
        document.getElementById("search-btn").style.display = "none";  // Masquer le bouton
    }
};

function search() {
    let game = document.getElementById("game-search").value.trim();
    let videoTitle = document.getElementById("video-title-search").value.trim();
    let channel = document.getElementById("channel-search").value.trim();
    let dateRange = document.getElementById("datepicker").value.trim();
    let tags = document.getElementById("tags-search").value.trim();

    if (game) activeQueries["Game"] = game;
    if (videoTitle) activeQueries["Video title"] = videoTitle;
    if (channel) activeQueries["Channel"] = channel;
    if (dateRange) activeQueries["Date"] = dateRange;
    if (tags) activeQueries["Tags"] = tags;

    updateActiveQueries();

    performSearch();
}

function updateActiveQueries() {
    let queryContainer = document.getElementById("active-queries");
    queryContainer.innerHTML = '';

    for (let key in activeQueries) {
        let queryValue = activeQueries[key];
        let button = document.createElement('button');
        button.innerHTML = `${key}: ${queryValue} <span onclick="removeQuery('${key}')">✖</span>`;
        queryContainer.appendChild(button);
    }
}

function removeQuery(key) {
    delete activeQueries[key];
    updateActiveQueries();
    performSearch();
}

function performSearch() {

    let searchParams = new URLSearchParams(activeQueries).toString();
    let url = `http://localhost:5000/search?${searchParams}`;

    window.location.href = url;
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