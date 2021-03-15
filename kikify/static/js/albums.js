async function openAlbums(url, isRecordLabel) {
    const csrftoken = getCookie('csrftoken');

    const albumsResponse = await fetch(url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({isRecordLabel:isRecordLabel})
    })
    const albumsHtml = await albumsResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = albumsHtml

    // set state
    states.push({
        url: url,
        unit: "album",
        command: async () => await openAlbums(url, isRecordLabel)
    })
}

async function openAlbum(url, artistId, albumId, isRecordLabel) {
    const csrftoken = getCookie('csrftoken');
    const albumResponse = await fetch(url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({isRecordLabel:isRecordLabel})
    })
    const albumHtml = await albumResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = albumHtml

    // set state
    states.push({
        url: url,
        unit: "song",
        command: async () => await openAlbum(url, artistId, albumId, isRecordLabel)
    })
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
                alert("Album not found.")
            else if(response.status === 200)
            {
                let data = await response.json()
                if(!data.show) {
                    alert("Album cannot be deleted")
                    return;
                }
                let poppedStated;
                let found = false;
                while (states.length!==0 && !found) {
                    poppedStated = states.pop()
                    if(poppedStated.unit===data.show){
                        found = true;
                    }
                }
                if(found){
                    alert("Album is successfully deleted. 😀")
                    await poppedStated.command()
                }else{
                    alert("Album cannot be deleted")
                }
            }
            else
                alert("Album cannot be deleted")
        } catch (e) {
            alert("Album cannot be deleted")
        }
    } else {
        alert("Ok.")
    }
}

async function editAlbum(event, url, id, name, artist) {
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
                    artist: artist
                })
            })
            if (response.status === 204)
                alert("Album not found.")
            else if (response.status === 200) {
                let data = await response.json()
                if (!data.show) {
                    alert("Album cannot be edited")
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
                    alert("Album is successfully edited. 😀")
                    $('#editAlbumModal').modal('hide');
                    await poppedStated.command()
                } else {
                    alert("Album cannot be edited")
                }
            } else
                alert("Album cannot be edited")
        } catch (e) {
            alert("Album cannot be edited")
        }
    } else {
        alert("Ok.")
    }
}