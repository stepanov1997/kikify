const playSong = (id) => {
    const player = document.getElementById('player')
    const playerSource = document.getElementById('playerSource')
    playerSource.setAttribute('src', `${location.protocol}//${location.host}/song/${id}/`)
    player.load(); //call this to just preload the audio without playing
    player.play(); //call this to play the song right away
}