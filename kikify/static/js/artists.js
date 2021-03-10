async function openArtists(url, isRecordLabel) {
    const csrftoken = getCookie('csrftoken');
    const artistsResponse = await fetch(url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({isRecordLabel:isRecordLabel})
    })
    const html = await artistsResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = html;

    // set state
    states.push({
        url: url,
        unit: "artist",
        command: async () => await openArtists(url, isRecordLabel)
    })
}

async function openArtist(url, artistId, isRecordLabel) {
    const csrftoken = getCookie('csrftoken');
    const artistResponse = await fetch(url, {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({isRecordLabel:isRecordLabel})
    })
    const artistHtml = await artistResponse.text()
    document.getElementsByClassName("content")[0].innerHTML = artistHtml

    // set state
    states.push({
        url: url,
        unit: "album",
        command: async () => await openArtist(url, artistId, isRecordLabel)
    })
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
            else if(response.status === 200)
            {
                let data = await response.json()
                if(!data.show) {
                    alert("Artist cannot be deleted")
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
                    alert("Artist is successfully deleted. 😀")
                    await poppedStated.command()
                }else{
                    alert("Artist cannot be deleted")
                }
            }
            else
                alert("Artist cannot be deleted")
        } catch (e) {
            alert("Artist cannot be deleted")
        }
    } else {
        alert("Ok.")
    }
}

async function editArtist(url, name, artistId) {
    if (confirm(`Are you sure you want to edit artist "${name}"?`)) {
        alert("Artist edited.")
    } else {
        alert("Ok.")
    }
}
