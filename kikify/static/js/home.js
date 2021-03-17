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

    // $("#menu-toggle").click(function (e) {
    //     e.preventDefault();
    //     $("#wrapper").toggleClass("toggled");
    // });
    if (isUser) {
        const isRecordLabel = !isUser
        await openArtists(url, isRecordLabel)
    } else {
        const isRecordLabel = !isUser
        await openArtists(url, isRecordLabel)
    }

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
                return JSON.stringify(getJSON(elem)).toLowerCase().includes(searchBar.value).toLowerCase()
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
            document.getElementById("imageResultModal").src = imageSrc
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
            for (var obj in postReqBody) {
                formData.append(obj, postReqBody[obj])
            }
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

        $('#edit-album-name').val(data.album)
        $('#edit-album-artist').val(data.artist)
        $('#edit-album-art').attr('src', `data:image/png;base64, ${data.picture}`)
    }
}

function removeSongForUploading(event, fileName, id) {
    event.preventDefault()
    $(`#${fileName}`).remove()
    files_for_upload = files_for_upload.filter(elem => elem.id !== id)
    return false
}

function uploadAlbum(event) {
    // const alertBox = document.getElementById('alert-box')
    // const imageBox = document.getElementById('image-box')
    // const progressBox = document.getElementById('progress-box')
    // const cancelBox = document.getElementById('cancel-box')
    // const cancelBtn = document.getElementById('cancel-btn')
    // $.ajax({
    //     type: 'POST',
    //     url: event.target.action,
    //     enctype: 'multipart/form-data',
    //     data: fd,
    //     beforeSend: function () {
    //         console.log('before')
    //     },
    //     xhr: function () {
    //         const xhr = new window.XMLHttpRequest();
    //         xhr.upload.addEventListener('progress', e => {
    //             // console.log(e)
    //             if (e.lengthComputable) {
    //                 const percent = e.loaded / e.total * 100
    //                 console.log(percent)
    //                 progressBox.innerHTML = `<div class="progress">
    //                                             <div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
    //                                         </div>
    //                                         <p>${percent.toFixed(1)}%</p>`
    //             }
    //
    //         })
    //         cancelBtn.addEventListener('click', () => {
    //             xhr.abort()
    //             setTimeout(() => {
    //                 event.target.reset()
    //                 progressBox.innerHTML = ""
    //                 alertBox.innerHTML = ""
    //                 cancelBox.classList.add('not-visible')
    //             }, 2000)
    //         })
    //         return xhr
    //     },
    //     success: function (response) {
    //         console.log(response)
    //         imageBox.innerHTML = `<img src="${url}" width="300px">`
    //         alertBox.innerHTML = `<div class="alert alert-success" role="alert">
    //                                 Successfully uploaded the image below
    //                             </div>`
    //         cancelBox.classList.add('not-visible')
    //     },
    //     error: function (error) {
    //         console.log(error)
    //         alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
    //                                 Ups... something went wrong
    //                             </div>`
    //     },
    //     cache: false,
    //     contentType: false,
    //     processData: false,
    // })
}
