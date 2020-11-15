/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}


/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */

let input;
let infoArea;

$(document).ready(function(){
    $('#upload').on('change', () => readURL(input));
    input = document.getElementById('upload');
    infoArea = document.getElementById('upload-label');

    input.addEventListener('change', showFileName);
})


function showFileName(event) {
    var input = event.srcElement;
    var fileName = input.files[0].name;
    fileNameSplited = fileName.split(".")
    infoArea.textContent = 'File name: ' + fileNameSplited[0].slice(0, 10) + "..."+ fileNameSplited[1];
    $("#upload-label").removeAttr("style")
    $(input).removeAttr("style")
    $(infoArea).removeAttr("style")
}