let states = []
let songs = []

const loadPage = async (url) => {
    window.onload = function() {
        document.getElementById("menu-toggle").addEventListener("click",  function(e){
        e.preventDefault();
        wrapper = document.getElementById("wrapper").classList;
        if(wrapper.contains("toggled"))
            wrapper.remove("toggled")
        else
            wrapper.add("toggled")
    });
    }

    // $("#menu-toggle").click(function (e) {
    //     e.preventDefault();
    //     $("#wrapper").toggleClass("toggled");
    // });
    await openArtists(url)
}


async function back() {
    if(states.length>1){
         states.pop()
        const state = states.pop()
        state.command()
    }
}

