async function openAlbums(url) {
    const albumsResponse = await fetch(url)
    const albumsHtml = await albumsResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = albumsHtml

    // set state
    states.push({
        url: url,
        unit: "album",
        command: async () => await openAlbums(url)
    })
}

async function openAlbum(url, artistId, albumId) {
    const albumResponse = await fetch(url)
    const albumHtml = await albumResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = albumHtml

    // set state
    states.push({
        url: url,
        unit: "song",
        command: async () => await openAlbum(url, artistId, albumId)
    })
}