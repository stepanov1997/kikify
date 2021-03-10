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
    if(isUser){
        const isRecordLabel = !isUser
        await openArtists(url, isRecordLabel)
    }else{
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
                        const getYear = elem => parseInt(elem => JSON.parse(elem.getElementsByClassName("artistJSON")[0].innerHTML).year)
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
                        const getYear = elem => parseInt(elem => JSON.parse(elem.getElementsByClassName("albumJSON")[0].innerHTML).year)
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
                        const getYear = elem => parseInt(elem => JSON.parse(elem.getElementsByClassName("songJSON")[0].innerHTML).year)
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

