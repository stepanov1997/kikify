function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function readSong(event, music_info_url) {
    let input = event.target
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = async function (e) {
            document.getElementById("sourceUploadedSong").src = e.target.result;
            const audio = document.getElementById("uploadedSong");
            audio.removeAttribute("hidden");
            audio.load();

            const filename = event.target.files[0].name
            document.getElementById("filename").innerText = `Filename: ${filename}`

            const csrftoken = getCookie('csrftoken');
            const formdata = new FormData();
            formdata.append("file", input.files[0], filename)

            const response = await fetch(music_info_url, {
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: formdata
            })

            if (response.status === 200) {
                let data = await response.json();
                console.log({data: data})
                document.getElementById("title").value = data.song;
                document.getElementById("album").value = data.album;
                document.getElementById("artist").value = data.artist;
                document.getElementById("imageResult").src = `data:image/png;base64, ${data.picture}`;
                document.getElementById("year").value = data.year;
            } else {
                document.getElementById("title").value = "";
                document.getElementById("album").value = "";
                document.getElementById("artist").value = "";
                document.getElementById("year").value = "";
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function readURLAlbumArt(event) {
    let input = event.target
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

async function uploadFile(event, url) {
    event.preventDefault()
    const image = document.getElementById("imageResult").src.split(",")[1]
    let formdata = new FormData();
    const submitFields = {
        title: document.getElementById("title").value,
        album: document.getElementById("album").value,
        artist: document.getElementById("artist").value,
        year: document.getElementById("year").value,
        upload: document.getElementById("upload").files[0],
        upload_art: image,
    }

    for(const key in submitFields){
        formdata.append(key, submitFields[key])
    }

    const csrftoken = getCookie('csrftoken');

    const response = await fetch(url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: formdata
    })

    const data = await response.json()

    console.log(data)

    closeForm()

    confirm("Uploading song was successful.")

    location.reload()

    return false
}