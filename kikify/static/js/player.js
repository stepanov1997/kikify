let currentPlayList = [];

const audio = new Audio();
let shuffle = false;

function changeMusicSongAlbumArt(url) {
    currentPlayList.forEach(elem => {
        if (elem && elem.album_art) {
            let song_div = document.getElementById(elem.id)
            if (song_div.getElementsByTagName("img")[0].src !== elem.album_art) {
                song_div.getElementsByTagName("img")[0].src = elem.album_art;
            }
        }
    })
    let song_div = document.getElementById(currentPlayList[0].id)
    currentPlayList[0].album_art = song_div.getElementsByTagName("img")[0].src
    //song_div.getElementsByTagName("img")[0].src = '/static/icons/song.svg'
    song_div.getElementsByTagName("img")[0].src = '/static/icons/current-song.gif'
}

const playSong = async (url, name, album, artist, isClick) => {
    audio.src = url;

    const playBtn = document.querySelector(".toggle-play");
    playBtn.classList.remove("play");
    playBtn.classList.add("pause");
    playBtn.setAttribute('src', '/static/icons/pause.svg')

    const value = parseFloat(document.getElementById('myRange').value)
    let newValue = (value / 101).toFixed(3)
    if (newValue > 0.95) newValue = 1;
    else if (newValue < 0.05) newValue = 0;
    audio.volume = parseFloat(newValue);

    await audio.play();

    if (isClick)
        createPlaylistFromSongs(url, shuffle);

    changeMusicSongAlbumArt(url)

    let text = document.createElement("p");
    text.innerHTML = `<i>${artist.toUpperCase()}</i> - <b>${name}</b> (${album}) `
    document.getElementById("song-info").innerHTML = text.outerHTML

    songs.push({
        url: url,
        name: name,
        album: album,
        artist: artist,
        command: async () => await playSong(url, name, album, artist)
    })
}

const createPlaylistFromSongs = (currentSongUrl, shuffle = false) => {
    currentPlayList.forEach(elem => {
        if (elem && elem.album_art) {
            let song_div = document.getElementById(elem.id)
            if (song_div && song_div.getElementsByTagName("img")[0].src !== elem.album_art) {
                song_div.getElementsByTagName("img")[0].src = elem.album_art;
            }
        }
    })
    const songsURLs = document.getElementsByClassName("songJSON");
    let temp = Array.from(songsURLs).map(elem => JSON.parse(elem.innerHTML));
    if (shuffle) {
        temp = temp.sort((a, b) => Math.random() - 0.5);
        temp = temp.sort((a, b) => Math.random() - 0.5);
        temp = temp.sort((a, b) => Math.random() - 0.5);
    }
    index = temp.findIndex(p => p.url === currentSongUrl)
    const temp2 = []
    for (let i = 0; i < temp.length; i++) {
        if (i >= index) {
            temp2.push(temp[i])
        }
    }
    for (let i = 0; i < temp.length; i++) {
        if (i < index) {
            temp2.push(temp[i])
        }
    }
    currentPlayList = temp2
}

async function playNextSong() {
    if (currentPlayList.length !== 0) {
        shifted = currentPlayList.shift()
        if (currentPlayList.length !== 0) {
            currentPlayList.push(shifted)
            nextSong = currentPlayList[0]
            await playSong(nextSong.url, nextSong.name, nextSong.album, nextSong.artist, false)
        }
    }
}


let oldPosition;

function volumeMute() {
    let range = document.getElementById("myRange")
    if (audio.muted)
        range.value = oldPosition
    else {
        oldPosition = parseFloat(range.value)
        range.value = 0
    }
    audio.muted = !audio.muted
}

function volumeMax() {
    audio.muted = false
    let range = document.getElementById("myRange")
    range.value = 100
    audio.volume = 1
}

function turnOnShuffle() {
    shuffle = !shuffle
    const icon = document.getElementById('shuffle-icon')
    if (shuffle) {
        icon.classList.replace("shuffle-disabled", "shuffle-enabled")

    } else {
        icon.classList.replace("shuffle-enabled", "shuffle-disabled")
    }
    if (currentPlayList.length !== 0) {
        const currentAudio = currentPlayList[0]
        createPlaylistFromSongs(audio.src, shuffle)

        let newPlayerList = currentPlayList.filter(e => e.url !== currentAudio.url)
        newPlayerList.unshift(currentAudio)
        currentPlayList = newPlayerList
        changeMusicSongAlbumArt(audio.src)
    }

}

$(document).ready(function () {
    const updateVolume = function (x, vol) {
        var volume = $('.volume');
        var percentage;
        //if only volume have specificed
        //then direct update volume
        if (vol) {
            percentage = vol * 100;
        } else {
            var position = x - volume.offset().left;
            percentage = 100 * position / volume.width();
        }

        if (percentage > 100) {
            percentage = 100;
        }
        if (percentage < 0) {
            percentage = 0;
        }

        //update volume bar and video volume
        $('.volumeBar').css('width', percentage + '%');
        audio.volume = percentage / 100;

        //change sound icon based on volume
        if (audio.volume === 0) {
            $('.sound').removeClass('sound2').addClass('muted');
        } else if (audio.volume > 0.5) {
            $('.sound').removeClass('muted').addClass('sound2');
        } else {
            $('.sound').removeClass('muted').removeClass('sound2');
        }

    };

//turn 128 seconds into 2:08
    function getTimeCodeFromNum(num) {
        let seconds = parseInt(num);
        let minutes = parseInt(seconds / 60);
        seconds -= minutes * 60;
        const hours = parseInt(minutes / 60);
        minutes -= hours * 60;

        if (hours === 0) return `${minutes}:${String(seconds % 60).padStart(2, 0)}`;
        return `${String(hours).padStart(2, 0)}:${minutes}:${String(
            seconds % 60
        ).padStart(2, 0)}`;
    }

    const audioPlayer = document.querySelector(".audio-player");

    console.log(audio)
    audio.addEventListener(
        "loadeddata",
        () => {

            if (audio.src !== "") {
                audioPlayer.querySelector(".time .length").textContent = getTimeCodeFromNum(
                    audio.duration
                );
                //audio.volume = .75;
            }

        },
        false
    );

//click on timeline to skip around
    const timeline = audioPlayer.querySelector(".timeline");
    timeline.addEventListener("click", e => {
        const timelineWidth = window.getComputedStyle(timeline).width;
        const timeToSeek = e.offsetX / parseInt(timelineWidth) * audio.duration;
        audio.currentTime = timeToSeek;
    }, false);

//click volume slider to change volume
//     const volumeSlider = audioPlayer.querySelector(".audio-player .volume-slider");
//     volumeSlider.addEventListener('click', e => {
//         const sliderWidth = window.getComputedStyle(volumeSlider).width;
//         const newVolume = e.offsetX / parseInt(sliderWidth);
//         audio.volume = newVolume;
//         audioPlayer.querySelector(".audio-player .volume-percentage").style.width = newVolume * 100 + '%';
//     }, false)

    if (audio.src !== "") {
        audioPlayer.querySelector(".time .length").textContent = getTimeCodeFromNum(
            audio.duration
        );
    } else {
        audioPlayer.querySelector(".time .length").textContent = ""
    }
//check audio percentage and update time accordingly
    setInterval(async () => {
        if (audio.src !== "") {
            const progressBar = audioPlayer.querySelector(".progress");
            progressBar.style.width = audio.currentTime / audio.duration * 100 + "%";
            audioPlayer.querySelector(".time .current").textContent = getTimeCodeFromNum(
                audio.currentTime
            );
            if (progressBar.style.width === "100%") {
                playBtn.setAttribute('src', '/static/icons/play.svg')
                await playNextSong()
            }
        }
    }, 500);

//toggle between playing and pausing on button click
    const playBtn = audioPlayer.querySelector(".toggle-play");
    playBtn.addEventListener(
        "click",
        () => {
            if (audio.src !== "") {
                if (audio.paused) {
                    playBtn.classList.remove("play");
                    playBtn.classList.add("pause");
                    playBtn.setAttribute('src', '/static/icons/pause.svg')
                    audio.play();
                } else {
                    playBtn.classList.remove("pause");
                    playBtn.classList.add("play");
                    playBtn.setAttribute('src', '/static/icons/play.svg')
                    audio.pause();
                }
            }
        },
        false
    );

    const nextBtn = document.getElementById("next-img").onclick = async function () {
        await playNextSong();
        // document.getElementById(currentPlayList[0].id).setAttribute('tabindex', '-1')
        // document.getElementById(currentPlayList[0].id).focus()
    }

    let intervalo = undefined;
    const forward_song = document.getElementById("forward-img")
    const back_song = document.getElementById("back-img")
    forward_song.onclick = async () => {
        audio.pause();
        audio.currentTime += 10;
        await audio.play();
    }
    forward_song.onmousedown = () => {
        audio.pause();
        intervalo = setInterval(function () {
            audio.currentTime += 10;
        }, 200);
    };
    forward_song.onmouseup = back_song.onmouseup = async () => {
        clearInterval(intervalo);
        await audio.play();
    };


    back_song.onclick = async () => {
        audio.pause();
        audio.currentTime -= 10;
        await audio.play();
    }
    back_song.onmousedown = () => {
        audio.pause();
        intervalo = setInterval(function () {
            audio.currentTime -= 10;
        }, 200);
    };

    const prevBtn = document.getElementById("prev-img").onclick = async function () {
        let nextSong;
        if (currentPlayList.length !== 0) {
            nextSong = currentPlayList.pop()
            currentPlayList.unshift(nextSong)
            await playSong(nextSong.url, nextSong.name, nextSong.album, nextSong.artist, false)
        }
    }

    var slider = document.getElementById("myRange");

    slider.oninput = function () {
        if (audio.volume > 0)
            audio.muted = false
        audio.volume = (this.value / 100).toFixed(3);
    }
    slider.onchange = function () {
        if (audio.volume > 0)
            audio.muted = false
        audio.volume = (this.value / 100).toFixed(3);
    }

})
;