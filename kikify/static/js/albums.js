async function openAlbums(url, isRecordLabel) {
    try {
        const csrftoken = getCookie('csrftoken');

        const albumsResponse = await fetch(url, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({isRecordLabel: isRecordLabel})
        })
        const albumsHtml = await albumsResponse.text()
        document.getElementsByClassName("content")[0].innerHTML = albumsHtml

        // set state
        states.push({
            url: url,
            unit: "album",
            command: async () => await openAlbums(url, isRecordLabel)
        })
    } catch (e) {
        kikifyAlert("Error", "Cannot open albums.")
    }
}

async function openAlbum(url, artistId, albumId, isRecordLabel) {
    try {
        const csrftoken = getCookie('csrftoken');
        const albumResponse = await fetch(url, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({isRecordLabel: isRecordLabel})
        })
        const albumHtml = await albumResponse.text()
        document.getElementsByClassName("content")[0].innerHTML = albumHtml

        // set state
        states.push({
            url: url,
            unit: "song",
            command: async () => await openAlbum(url, artistId, albumId, isRecordLabel)
        })
    } catch (e) {
        kikifyAlert("Error", "Cannot open album.")
    }

}

async function deleteAlbum(url, name, albumId) {
    if (confirm(`Are you sure you want to delete album "${name}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST'
            })
            if (response.status === 204)
                kikifyAlert("Error", "Album not found")
            else if (response.status === 200) {
                let data = await response.json()
                if (!data.show) {
                    kikifyAlert("Error", "Album cannot be deleted")
                    return;
                }
                let poppedStated;
                let found = false;
                while (states.length !== 0 && !found) {
                    poppedStated = states.pop()
                    if (poppedStated.unit === data.show) {
                        found = true;
                    }
                }
                if (found) {
                    kikifyAlert("Error", "Album is successfully deleted. 😀")
                    await poppedStated.command()
                } else {
                    kikifyAlert("Error", "Album cannot be deleted.")
                }
            } else
                kikifyAlert("Error", "Album cannot be deleted.")
        } catch (e) {
            kikifyAlert("Error", "Album cannot be deleted.")
        }
    } else {
        kikifyAlert("Information", "Ok.", "info")
    }
}

async function editAlbum(event, url, id, name, artist, imageaArt) {
    event.preventDefault()
    if (confirm(`Are you sure you want to edit album "${name}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST',
                body: JSON.stringify({
                    id: id,
                    name: name,
                    artist: artist,
                    imageArt: imageaArt.src.split(",")[1]
                })
            })
            if (response.status === 204)
                kikifyAlert("Error", "Album not found.")
            else if (response.status === 200) {
                let data = await response.json()
                if (!data.show) {
                    kikifyAlert("Error", "Album cannot be edited")
                    return;
                }
                let poppedStated;
                let found = false;
                while (states.length !== 0 && !found) {
                    poppedStated = states.pop()
                    if (poppedStated.unit === data.show) {
                        found = true;
                    }
                }
                if (found) {
                    kikifyAlert("Successfully edit", "Album is successfully edited. 😀", "success")
                    $('#editAlbumModal').modal('hide');
                    await poppedStated.command()
                } else {
                    kikifyAlert("Error", "Album cannot be edited")
                }
            } else
                kikifyAlert("Error", "Album cannot be edited")
        } catch (e) {
            kikifyAlert("Error", "Album cannot be edited")
        }
    } else {
        kikifyAlert("Information", "Ok", "info")
    }
}