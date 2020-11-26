async function openSongs(url) {
    const songsResponse = await fetch(url)
    document.getElementsByClassName("content")[0].innerHTML = await songsResponse.text()

    // set state
    states.push({
        url: url,
        unit: 'song',
        command: async () => await openSongs(url)
    })
}