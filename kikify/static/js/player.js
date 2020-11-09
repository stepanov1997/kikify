const playSong = (url, name, album, artist) => {
    const player = document.getElementById('player')
    const playerSource = document.getElementById('playerSource')
    playerSource.setAttribute('src', url)
    player.load(); //call this to just preload the audio without playing
    player.play(); //call this to play the song right away

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