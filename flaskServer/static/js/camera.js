window.onload = function() {
    var video = document.createElement("video");
    var canvasElement = document.getElementById("canvas");
    var canvas = canvasElement.getContext("2d");
    var loadingMessage = document.getElementById("loadingMessage");
    var outputContainer = document.getElementById("output");
    var outputMessage = document.getElementById("outputMessage");
    var outputData = document.getElementById("outputData");
    var isPosted = undefined;

    function drawLine(begin, end, color) {
        canvas.beginPath();
        canvas.moveTo(begin.x, begin.y);
        canvas.lineTo(end.x, end.y);
        canvas.lineWidth = 4;
        canvas.strokeStyle = color;
        canvas.stroke();
    }
    
    // Use facingMode: environment to attemt to get the front camera on phones
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
        video.srcObject = stream;
        video.setAttribute("playsinline", true);// required to tell iOS safari we don't want fullscreen
        video.play();
        requestAnimationFrame(tick);
    });

    function postForm(qrcodeData, base64) {
        var form = document.createElement('form');
        var field1 = document.createElement('input');
        var field2 = document.createElement('input');
        form.method = 'POST';
        form.action = '/authQRcode';
        field1.type = 'hidden';
        field1.name = 'qrcodeData';
        field1.value = qrcodeData;
        field2.type = 'hidden';
        field2.name = 'base64';
        field2.value = base64;
        form.appendChild(field1);
        form.appendChild(field2);
        document.body.appendChild(form);
        form.submit();
    }

    function tick() {
        loadingMessage.innerText = "読み込み中..."
        if (video.readyState === video.HAVE_ENOUGH_DATA && typeof isPosted === "undefined") {
            loadingMessage.hidden = true;
            canvasElement.hidden = false;
            outputContainer.hidden = false;
            canvasElement.height = video.videoHeight;
            canvasElement.width = video.videoWidth;
            canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
            var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
            var code = jsQR(imageData.data, imageData.width, imageData.height, {
              inversionAttempts: "dontInvert",
            });
            if (code) {
                drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
                drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
                drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
                drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
                outputMessage.hidden = true;
                outputData.parentElement.hidden = false;
                outputData.innerText = code.data;
                const canvasBase64 = canvasElement.toDataURL('image/png');
                //send_data(code.data, canvasBase64);

                $("#video").remove();
                $("#canvas").remove();
                postForm(code.data, canvasBase64);
                isPosted = true;

                //location.href = '/authResult';
            } else {
                outputMessage.hidden = false;
                outputData.parentElement.hidden = true;
            }
        }
        requestAnimationFrame(tick);
    }
}