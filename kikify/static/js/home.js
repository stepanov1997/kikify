let states = []
let songs = []

const loadPage = async (url, isUser) => {
    window.onload = function () {
        document.getElementById("menu-toggle").addEventListener("click", function (e) {
            e.preventDefault();
            wrapper = document.getElementById("wrapper").classList;
            if (wrapper.contains("toggled"))
                wrapper.remove("toggled")
            else
                wrapper.add("toggled")
        });
    }
    const isRecordLabel = !isUser
    await openArtists(url, isRecordLabel)
}

function sortSongs(key) {
    let songsContainer = document.getElementsByClassName("songs-container")[0]
    let artistContainer = document.getElementsByClassName("artists-container")[0]
    let albumContainer = document.getElementsByClassName("albums-container")[0]
    let currentUnit = states[states.length - 1].unit;
    switch (key.toLowerCase()) {
        case "title": {
            switch (currentUnit) {
                case "artist": {
                    sorted = Array.from(artistContainer.children).sort((a, b) => {
                        const getName = elem => JSON.parse(elem.getElementsByClassName("artistJSON")[0].innerHTML).name
                        return getName(a).localeCompare(getName(b))
                    })
                    artistContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        artistContainer.appendChild(elem)
                    })
                }
                    break;
                case "album": {
                    sorted = Array.from(albumContainer.children).sort((a, b) => {
                        const getName = elem => JSON.parse(elem.getElementsByClassName("albumJSON")[0].innerHTML).name
                        return getName(a).localeCompare(getName(b))
                    })
                    albumContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        albumContainer.appendChild(elem)
                    })
                }
                    break;
                case "song": {
                    sorted = Array.from(songsContainer.children).sort((a, b) => {
                        const getName = elem => JSON.parse(elem.getElementsByClassName("songJSON")[0].innerHTML).name
                        return getName(a).localeCompare(getName(b))
                    })
                    songsContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        songsContainer.appendChild(elem)
                    })
                }
                    break;
            }
        }
            break;
        case "album": {
            switch (currentUnit) {
                case "artist": {
                    sorted = Array.from(artistContainer.children).sort((a, b) => {
                        const getAlbum = elem => JSON.parse(elem.getElementsByClassName("artistJSON")[0].innerHTML).album
                        return getAlbum(a).localeCompare(getAlbum(b))
                    })
                    artistContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        artistContainer.appendChild(elem)
                    })
                }
                    break;
                case "album": {
                    sorted = Array.from(albumContainer.children).sort((a, b) => {
                        const getAlbum = elem => JSON.parse(elem.getElementsByClassName("albumJSON")[0].innerHTML).album
                        return getAlbum(a).localeCompare(getAlbum(b))
                    })
                    albumContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        albumContainer.appendChild(elem)
                    })
                }
                    break;
                case "song": {
                    sorted = Array.from(songsContainer.children).sort((a, b) => {
                        const getAlbum = elem => JSON.parse(elem.getElementsByClassName("songJSON")[0].innerHTML).album
                        return getAlbum(a).localeCompare(getAlbum(b))
                    })
                    songsContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        songsContainer.appendChild(elem)
                    })
                }
                    break;
            }
        }
            break;
        case "artist": {
            switch (currentUnit) {
                case "artist": {
                    sorted = Array.from(artistContainer.children).sort((a, b) => {
                        const getArtist = elem => JSON.parse(elem.getElementsByClassName("artistJSON")[0].innerHTML).artist
                        return getArtist(a).localeCompare(getArtist(b))
                    })
                    artistContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        artistContainer.appendChild(elem)
                    })
                }
                    break;
                case "album": {
                    sorted = Array.from(albumContainer.children).sort((a, b) => {
                        const getArtist = elem => JSON.parse(elem.getElementsByClassName("albumJSON")[0].innerHTML).artist
                        return getArtist(a).localeCompare(getArtist(b))
                    })
                    albumContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        albumContainer.appendChild(elem)
                    })
                }
                    break;
                case "song": {
                    sorted = Array.from(songsContainer.children).sort((a, b) => {
                        const getArtist = elem => JSON.parse(elem.getElementsByClassName("songJSON")[0].innerHTML).artist
                        return getArtist(a).localeCompare(getArtist(b))
                    })
                    songsContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        songsContainer.appendChild(elem)
                    })
                }
                    break;
            }
        }
            break;
        case "year": {
            switch (currentUnit) {
                case "artist": {
                    sorted = Array.from(artistContainer.children).sort((a, b) => {
                        const getYear = elem => parseInt(JSON.parse(elem.getElementsByClassName("artistJSON")[0].innerHTML).year)
                        return getYear(a) - getYear(b)
                    })
                    artistContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        artistContainer.appendChild(elem)
                    })
                }
                    break;
                case "album": {
                    sorted = Array.from(albumContainer.children).sort((a, b) => {
                        const getYear = elem => parseInt(JSON.parse(elem.getElementsByClassName("albumJSON")[0].innerHTML).year)
                        return getYear(a) - getYear(b)
                    })
                    albumContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        albumContainer.appendChild(elem)
                    })
                }
                    break;
                case "song": {
                    sorted = Array.from(songsContainer.children).sort((a, b) => {
                        const getYear = elem => parseInt(JSON.parse(elem.getElementsByClassName("songJSON")[0].innerHTML).year)
                        return getYear(a) - getYear(b)
                    })
                    songsContainer.innerHTML = ""
                    sorted.forEach(elem => {
                        songsContainer.appendChild(elem)
                    })
                }
                    break;
            }
        }
            break;

    }
}

// $(".content").ready(function () {
//     $('.content').bind('DOMSubtreeModified', function () {
//         if(!states[states.length - 1]) return
//         switch (states[states.length - 1].unit) {
//             case "artist": {
//                 Array.from($(`#sort_a dropdown-item`).children).forEach(elem => {
//                     if (elem.innerText.toLowerCase().includes("artist"))
//                         elem.show()
//                     else
//                         elem.hide()
//                 })
//             }
//                 break;
//             case "album": {
//                 Array.from($('dropdown-item').children).forEach(elem => {
//                     if (elem.innerText.toLowerCase().includes("title"))
//                         elem.hide()
//                     else
//                         elem.show()
//                 })
//             }
//                 break;
//             case "song": {
//                 Array.from($('dropdown-item').children).forEach(elem => elem.show())
//             }
//                 break;
//         }
//     });
// })

async function search_input(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        search()
    }
}

async function search() {
    await states[states.length - 1].command()
    searchBar = document.getElementById("searchBar")
    let songsContainer = document.getElementsByClassName("songs-container")[0]
    let artistContainer = document.getElementsByClassName("artists-container")[0]
    let albumContainer = document.getElementsByClassName("albums-container")[0]
    let currentUnit = states[states.length - 1].unit;
    switch (currentUnit) {
        case "artist": {
            sorted = Array.from(artistContainer.children).filter(elem => {
                const getJSON = elem1 => JSON.parse(elem1.getElementsByClassName("artistJSON")[0].innerHTML)
                return JSON.stringify(getJSON(elem)).toLowerCase().includes(searchBar.value.toLowerCase())
            })
            artistContainer.innerHTML = ""
            sorted.forEach(elem => {
                artistContainer.appendChild(elem)
            })
        }
            break;
        case "album": {
            sorted = Array.from(albumContainer.children).filter(elem => {
                const getJSON = elem1 => JSON.parse(elem1.getElementsByClassName("albumJSON")[0].innerHTML)
                return JSON.stringify(getJSON(elem)).toLowerCase().includes(searchBar.value.toLowerCase())
            })
            albumContainer.innerHTML = ""
            sorted.forEach(elem => {
                albumContainer.appendChild(elem)
            })
        }
            break;
        case "song": {
            sorted = Array.from(songsContainer.children).filter(elem => {
                const getJSON = elem1 => JSON.parse(elem1.getElementsByClassName("songJSON")[0].innerHTML)
                return JSON.stringify(getJSON(elem)).toLowerCase().includes(searchBar.value.toLowerCase())
            })
            songsContainer.innerHTML = ""
            sorted.forEach(elem => {
                songsContainer.appendChild(elem)
            })
        }
            break;
    }
}

async function back() {
    if (states.length > 1) {
        states.pop()
        const state = states.pop()
        state.command()
    }
}

function _readFileDataUrl(input, callback) {
    const len = input.files.length, _files = [], res = [];
    const readFile = function (filePos) {
        if (!filePos) {
            callback(false, res);
        } else {
            const reader = new FileReader();
            reader.onload = function (e) {
                res.push({id: res.length, file: filePos, base64: e.target.result});
                readFile(_files.shift());
            };
            reader.readAsDataURL(filePos);
        }
    };
    for (let x = 0; x < len; x++) {
        _files.push(input.files[x]);
    }
    readFile(_files.shift());
}

let files_for_upload = [];

$(document).ready(() => {
    $('#uploadModal').on('change', function () {
        _readFileDataUrl(this, async function (err, files) {
            if (err) {
                return
            }
            files_for_upload = files
            await populateUploadAlbumForm(files)
        });
    });
    $('#editSongModal').on('show.bs.modal', async e => {
        const songid = $(e.relatedTarget).data('content')
        await populateEditForm(songid);
    });
    $('#editAlbumModal').on('show.bs.modal', async e => {
        const albumId = $(e.relatedTarget).data('content')
        await populateEditForm(albumId);
    });
    $('#editArtistModal').on('show.bs.modal', async e => {
        const artistId = $(e.relatedTarget).data('content')
        await populateEditForm(artistId);
    });
    $('#editProfileModal').on('show.bs.modal', async e => {
        const url = $(e.relatedTarget).data('content')
        await populateProfileEditForm(url);
    });
    $('#changePasswordModal').on('show.bs.modal', async e => {
        const url = $(e.relatedTarget).data('content')
        // await populateChangePasswordForm(url);
    });

})

async function populateEditForm(id) {
    const div = document.getElementById(id)
    const unit = states[states.length - 1].unit

    const jsonInput = div.getElementsByClassName(`${unit}JSON`)[0].innerHTML
    const infos = JSON.parse(jsonInput)
    switch (unit) {
        case 'song': {
            document.getElementById("edit-song-id").value = infos.id
            document.getElementById("edit-song-title").value = infos.name
            document.getElementById("edit-song-album").value = infos.album
            document.getElementById("edit-song-artist").value = infos.artist
        }
            break;
        case 'album': {
            const imageSrc = div.getElementsByClassName("album-art")[0].src
            document.getElementById("edit-album-id").value = infos.id
            document.getElementById("edit-album-name").value = infos.name
            document.getElementById("edit-album-artist").value = infos.artist
            document.getElementById("edit-album-art").src = imageSrc
        }
            break;
        case 'artist': {
            document.getElementById("edit-artist-id").value = infos.id
            document.getElementById("edit-artist-name").value = infos.name
        }
            break;
        default: {

        }
    }
}

async function populateProfileEditForm() {
    const sidebar = document.getElementsByClassName("sidebar")[0]
    const image = sidebar.getElementsByClassName("album-art")[0]
    document.getElementById("imageResultProfileModal").src = image.src
    document.getElementById("edit-first-name").value = profile.firstname
    document.getElementById("edit-second-name").value = profile.secondname
    document.getElementById("edit-username").value = profile.username
    document.getElementById("edit-email").value = profile.email
}

async function editProfile(event, url, firstName, secondName, username, email, password, image, isUser) {
    event.preventDefault()
    if (confirm(`Are you sure you want to edit profile "${username}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            const postReqBody = {
                firstName: firstName,
                secondName: secondName,
                username: username,
                email: email,
                password: password,
                isUser: isUser
            }
            var formData = new FormData();
            for (const obj in postReqBody) {
                formData.append(obj, postReqBody[obj])
            }
            if (image.files.length !== 0)
                formData.append("profilePicture", image.files[0])

            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST',
                body: formData
            })
            if (response.status === 204)
                alert("Entered password is not ok.")
            else if (response.status === 200) {
                let data = await response.json()
                if (!data) {
                    alert("Profile cannot be edited")
                    return;
                }
                alert("Profile is successfully edited. 😀")
                $('#editSongModal').modal('hide');
                location.reload()

            } else
                alert("Profile cannot be edited")
        } catch (e) {
            alert("Profile cannot be edited")
        }
    } else {
        alert("Ok.")
    }
}

async function updatePassword(event, url, oldPassword, newPassword1, newPassword2) {
    event.preventDefault()
    if (confirm(`Are you sure you want to change password of profile "${profile.username}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            if (newPassword1 !== newPassword2) {
                alert("New passwords should be the same.")
                return;
            }
            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST',
                body: JSON.stringify({
                    oldpassword: oldPassword,
                    newpassword1: newPassword1,
                    newpassword2: newPassword2
                })
            })
            if (response.status === 204)
                alert("Entered password is not ok.")
            else if (response.status === 200) {
                alert("Password is successfully changed. 😀")
                $('#editSongModal').modal('hide');
                location.reload()

            } else
                alert("Password cannot be changed")
        } catch (e) {
            alert("Password cannot be changed")
        }
    } else {
        alert("Ok.")
    }
}

async function populateUploadAlbumForm(files) {
    const table = `
    <table class="table">
        <thead>
            <tr>
                <th>Song name</th>
                <th>Player</th>
                <th>Size</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            ${files.map((file, i) => `
            <tr id="song-upload-${file.id}">
                <td>${file.file.name}</td>
                <td><audio src="${file.base64}" controls></audio></td>
                <td>${(file.file.size / 1024 / 1024).toFixed(1)} MB</td>
                <td><button type="button" onclick="return removeSongForUploading(event, 'song-upload-${file.id}', ${file.id})">Delete</button></td>
            </tr>
            `).reduce((a, b) => a + b, "")}
        </tbody>
    </table>`

    $("#songs-for-upload").html(table)

    const csrftoken = getCookie('csrftoken');
    const formdata = new FormData();
    formdata.append("file", files[0].file, files[0].file.name)

    const response = await fetch(urls.music_info_url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: formdata
    })

    if (response.status === 200) {
        let data = await response.json();
        console.log({data: data})

        $('#upload-album-name').val(data.album)
        $('#upload-album-artist').val(data.artist)
        $('#upload-album-year').val(data.year)
        $('#upload-album-art').attr('src', `data:image/png;base64, ${data.picture}`)
    }
}

function removeSongForUploading(event, fileName, id) {
    event.preventDefault()
    $(`#${fileName}`).remove()
    files_for_upload = files_for_upload.filter(elem => elem.id !== id)
    return false
}

function uploadAlbum(event, url, name, album, artist, year, image) {
    event.preventDefault()
    const csrftoken = getCookie('csrftoken');

    console.log('Upload function begins');
    let pBar = document.getElementsByClassName('progress-bar')[0],
        formData = new FormData(),
        xhr = new XMLHttpRequest(),
        percent = 0;

    formData.append("name", name)
    formData.append("album", album)
    formData.append("artist", artist)
    formData.append("year", year)
    formData.append("image", image.src.split(", ")[1])
    for (const file of files_for_upload) {
        formData.append(`file${file.id}`, file.file)
    }

    console.log('Form Data created');
    // Start upload
    xhr.upload.onloadstart = function () {

    };

    // Track upload progress
    xhr.upload.onprogress = function (event) {
        percent = parseInt(event.loaded / event.total * 100);
        pBar.innerHTML = percent + "%";
        pBar.style.width = percent + "%";
        console.log(percent + '% completed');
        console.log('Uploaded event.loaded of event.total');
    };

    // Report if ends with an error
    xhr.upload.onerror = function () {
        console.log('An error has occurred')
    };

    // Track completion: Both successful or not
    xhr.upload.onloadend = function () {
        console.log('Upload complete with or without error ' + xhr.status);
    };

    // Track progress: Triggered on successful completion
    xhr.upload.onload = function () {
        console.log('Uploading complete');
    };

    xhr.open("POST", url, true);

    xhr.onreadystatechange = function () {
        if (this.status === 200 && this.readyState === 4) {
            let jsonResponse = JSON.parse(this.response)
            if (jsonResponse.message === "success") {
                $('.alert').alert()
                $('#uploadAlbumModalLabel').modal('hide');
                location.reload()

            }
        }
    }

    // The 'setRequestHeader' function can only be called when xhr is opened.
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.send(formData);
}

function kikifyAlert(header, message, type) {
    // $("#alert-header").text(header)
    // $("#alert-message").text(message)
    // if(type)
    //     $("#alertModal").classList.add(type)
    // $("#alertModal").show()
    alert(message)
}
