$(document).ready(function() {

    $('.searchable-column').on('click', function() {
        const searchField = $(this).data('search');

        $('.search-group').hide();

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

function search() {
    let game = document.getElementById("game-search").value.trim();
    let videoTitle = document.getElementById("video-title-search").value.trim();
    let channel = document.getElementById("channel-search").value.trim();
    let dateRange = document.getElementById("datepicker").value.trim();
    let tags = document.getElementById("tags-search").value.trim();

    if (game) activeQueries["game"] = game;
    if (videoTitle) activeQueries["video_title"] = videoTitle;
    if (channel) activeQueries["channel"] = channel;
    if (dateRange) activeQueries["date"] = dateRange;
    if (tags) activeQueries["tags"] = tags;

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