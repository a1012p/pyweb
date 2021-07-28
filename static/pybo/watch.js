// 디지털 시계 구현

setInterval(myWatch, 1000) //1초 간격으로 시간 설정

function myWatch(){
    var date = new Date();
    var now = date.toLocaleTimeString();
    var watch= document.getElementById("demo")
    watch.innerHTML = now;
    watch.style.display='block'
    document.getElementById("spin").style.display='none'

}