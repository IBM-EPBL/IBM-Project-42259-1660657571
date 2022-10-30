function form_create(){
    var elem=document.getElementById('add_elem')
    elem.innerHTML=`<div class=\"form-group\"><form action=\"url_for()\" method=\"post\"><label class=\"col-md-5\">Enter your query : </label><input class=\"form-control col-md-5\"
            type=\"textarea\" name=\"query\" id=\"query\">
        <input type=\"submit\" value=\"Submit\">
    </form>
</div>`
}
