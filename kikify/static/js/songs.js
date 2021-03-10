async function openSongs(url, isRecordLabel) {
    const csrftoken = getCookie('csrftoken');
    const songsResponse = await fetch(url, {
        headers: {"X-CSRFToken": csrftoken},
        method: 'POST',
        body: JSON.stringify({isRecordLabel: isRecordLabel})
    })
    document.getElementsByClassName("content")[0].innerHTML = await songsResponse.text()

    // set state
    states.push({
        url: url,
        unit: 'song',
        command: async () => await openSongs(url, isRecordLabel)
    })
}

async function deleteSong(url, name, songId) {
    if (confirm(`Are you sure you want to delete song "${name}"?`)) {
        const csrftoken = getCookie('csrftoken');
        try {
            const response = await fetch(url, {
                headers: {"X-CSRFToken": csrftoken},
                method: 'POST'
            })
            if (response.status === 204)
                alert("Song not found.")
            else if(response.status === 200)
            {
                let data = await response.json()
                if(!data.show) {
                    alert("Song cannot be deleted")
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
                    alert("Song is successfully deleted. 😀")
                    await poppedStated.command()
                }else{
                    alert("Song cannot be deleted")
                }
            }
            else
                alert("Song cannot be deleted")
        } catch (e) {
            alert("Song cannot be deleted")
        }
    } else {
        alert("Ok.")
    }
}

async function editSong(url, name, songId) {
    if (confirm(`Are you sure you want to edit song "${name}"?`)) {
        alert("Song edited.")
    } else {
        alert("Ok.")
    }
}