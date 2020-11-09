async function openSongs(url) {
    const songsResponse = await fetch(url)
    const songsHtml = await songsResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = songsHtml

    // set state
    states.push({
        url: url,
        command: async () => await openSongs(url)
    })
}