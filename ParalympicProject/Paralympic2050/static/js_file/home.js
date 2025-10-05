// Video play and audio gain (for the audio gain, getting it from stack overflow)
const video = document.querySelector(".video-play");

const audioContext = new (window.AudioContext || window.webkitAudioContext)();
const source = audioContext.createMediaElementSource(video);
const gainNode = audioContext.createGain();
source.connect(gainNode);
gainNode.connect(audioContext.destination);

gainNode.gain.value = 1.0;

document.addEventListener("click", function () {
    if (video.muted) {
        video.muted = false;
        audioContext.resume();
    } 
    else {
        video.muted = true;
    }
    video.play();
});
