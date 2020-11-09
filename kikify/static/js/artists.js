async function openArtists(url) {
    const artistsResponse = await fetch(url)
    const html = await artistsResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = html;

    // set state
    states.push({
        url: url,
        command: async () => await openArtists(url)
    })
}

async function openArtist(url, artistId) {
    const artistResponse = await fetch(url)
    const artistHtml = await artistResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = artistHtml

    // set state
    states.push({
        url: url,
        command: async () => await openArtist(url, artistId)
    })
}
