async function openArtists(url, isRecordLabel) {
    try {
        const csrftoken = getCookie('csrftoken');
        const artistsResponse = await fetch(url, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({isRecordLabel: isRecordLabel})
        })
        const html = await artistsResponse.text()
        document.getElementsByClassName("content")[0].innerHTML = html;

        // set state
        states.push({
            url: url,
            unit: "artist",
            command: async () => await openArtists(url, isRecordLabel)
        })
    } catch (e) {
        kikifyAlert("Error", "Cannot open artists.")
    }
}

async function openArtist(url, artistId, isRecordLabel) {
    try {
        const csrftoken = getCookie('csrftoken');
        const artistResponse = await fetch(url, {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({isRecordLabel: isRecordLabel})
        })
        const artistHtml = await artistResponse.text()
        document.getElementsByClassName("content")[0].innerHTML = artistHtml

        // set state
        states.push({
            url: url,
            unit: "album",
            command: async () => await openArtist(url, artistId, isRecordLabel)
        })
    } catch (e) {
        kikifyAlert("Error", "Cannot open artist.")
    }
}

async function deleteArtist(url, name, albumId) {
    if (confirm(`Are you sure you want to delete artist "${name}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST'
            })
            if (response.status === 204)
                alert("Artist not found.")
            else if (response.status === 200) {
                let data = await response.json()
                if (!data.show) {
                    kikifyAlert("Error", "Artist cannot be deleted.")
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
                    kikifyAlert("Artist deleted", "Artist is successfully deleted. 😀", "success")
                    await poppedStated.command()
                } else {
                    kikifyAlert("Error", "Artist cannot be deleted.")
                }
            } else
               kikifyAlert("Error", "Artist cannot be deleted.")
        } catch (e) {
            kikifyAlert("Error", "Artist cannot be deleted.")
        }
    } else {
        kikifyAlert("Information", "Ok.", "info")
    }
}

async function editArtist(event, url, id, name) {
    event.preventDefault()
    if (confirm(`Are you sure you want to edit artist "${name}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST',
                body: JSON.stringify({
                    id: id,
                    name: name,
                })
            })
            if (response.status === 204)
                kikifyAlert("Error", "Artist not found.")
            else if (response.status === 200) {
                let data = await response.json()
                if (!data.show) {
                    kikifyAlert("Error", "Artist not found.")
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
                    kikifyAlert("Artist edited", "Artist successfully edited.", "success")
                    $('#editAlbumModal').modal('hide');
                    await poppedStated.command()
                } else {
                    kikifyAlert("Error", "Artist not found.")
                }
            } else
               kikifyAlert("Error", "Artist cannot be edited.")
        } catch (e) {
            kikifyAlert("Error", "Artist cannot be edited.")
        }
    } else {
        kikifyAlert("Information", "Ok.", "info")
    }
}
