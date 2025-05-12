setInterval(() => {
    fetch("http://cepbep4-hopfild-cfed.twc1.net/getPhotos", {
        method: "GET"
    }).then(response => response.text()).then(answer => {
        load(JSON.parse(answer))
    })
}, 1000)

function update(){
    fetch("http://cepbep4-hopfild-cfed.twc1.net/getPhotos", {
        method: "GET"
    }).then(response => response.text()).then(answer => {
        load(JSON.parse(answer))
    })
}

function load(data){
    document.getElementById("vc1").innerHTML = ""
    for (let i = 0; i<data["image"].length; i++){
        document.getElementById("vc1").innerHTML += `
            <div class="vector">
                <img class="vector-image" src="${data["image"][i]["img_signal"]}" alt="">
                <div class="vector-text"><span>${data["image"][i]["str"]}</span></div>
            </div>
        `
    }

    document.getElementById("vc2").innerHTML = ""
    for (let i = 0; i<data["image"].length; i++){
        document.getElementById("vc2").innerHTML += `
            <div class="vector">
                <img class="test-img" src="${data["image"][i]["img_signal"]}" alt="">
                <img class="test-img" src="${data["image"][i]["img_render"]}" alt="">
            </div>
        `
    }
}