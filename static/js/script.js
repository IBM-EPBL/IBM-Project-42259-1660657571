function form_create() {
    var CONTINUE = confirm("DOING THIS WILL DELETE YOUR PREVIOUS QUERY.Do you want to continue?")
    if (CONTINUE === true) {
        var elem = document.getElementById('add_elem')
        elem.innerHTML = `<div class="container pd-20"><form action="/success" method="post">
        <div class="form-group"><label class="col-md-5">Enter your query : </label>
        <input name="query" class=\"form-control col-md-5\"type="textarea" name="query" id="query">
        <input type="submit" value="Submit"></div></form></div>`
    }

}
