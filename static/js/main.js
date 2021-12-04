
https://github.com/chrisguttandin/extendable-media-recorder

navigator
.mediaDevices
.getUserMedia({audio: true})
.then(stream => { handlerFunction(stream) });

function handlerFunction(stream) {
    rec = new MediaRecorder(stream, {type: 'audio/wav'});
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive") {
            let blob = new Blob(audioChunks, {type: 'audio/wav'});
            sendData(blob);
        }
    }
}

function sendData(data) {
    var form = new FormData();
    form.append('file', data, 'data.wav');
    form.append('title', 'data.wav');
    //Chrome inspector shows that the post data includes a file and a title.
    $.ajax({
        type: 'POST',
        url: '/saveRecord',
        data: form,
        cache: false,
        processData: false,
        contentType: false
    }).done(function(data) {
        document.write(data);
    });
}

startRecording.onclick = e => {
    console.log('Recording are started..');
    startRecording.disabled = true;
    stopRecording.disabled = false;
    audioChunks = [];
    rec.start();
    document.getElementById("msg").style.display = "inherit";
};

stopRecording.onclick = e => {
    console.log("Recording are stopped.");
    document.getElementById("msg").style.display = "none";
    startRecording.disabled = false;
    stopRecording.disabled = true;
    rec.stop();
    waitFunc();
};

function waitFunc() {
  alert("Kindly please wait for execution to complete");
}

