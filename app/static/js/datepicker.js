$( function() {
    $( "#datepicker" ).datepicker({
        dateFormat: 'yy-mm-dd'
    });
  }
);

function search_date() {

    let specific_date = document.getElementById("datepicker").value;
    window.location.href = `http://localhost:5000/search_date?date=${encodeURIComponent(specific_date)}`;
}