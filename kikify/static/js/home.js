let states = []
let songs = []

const loadPage = async (url) => {
    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    await openArtists(url)
}


async function back() {
    if(states.length>1){
         states.pop()
        const state = states.pop()
        state.command()
    }
}

