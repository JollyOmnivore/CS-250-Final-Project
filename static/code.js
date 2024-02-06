
var count = 5;
function changeImage() {
    var image = document.getElementById('funnyfish');
    var link =  document.getElementById('fishlink');
        if (image.src.match("/static/fish.gif")) {
            alert("You Found it press ok to continue")
            count++
            if (count >= 5){
                link.href = "/secret";
            }
        }
}
