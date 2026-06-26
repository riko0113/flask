const video = document.getElementById("video");

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri("static/models"),
  faceapi.nets.faceLandmark68Net.loadFromUri("static/models"),
  faceapi.nets.faceRecognitionNet.loadFromUri("static/models"),
  faceapi.nets.faceExpressionNet.loadFromUri("static/models"),
  faceapi.nets.ageGenderNet.loadFromUri("static/models"),
]).then(startVideo);

function startVideo() {
  console.log("startVideo実行");

  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      console.log("カメラ取得成功");
      video.srcObject = stream;
    })
    .catch(function (err) {
      console.error("カメラエラー:", err);
    });
}

let isRedirecting = false;

video.addEventListener("playing", () => {
  let canvas = document.querySelector("canvas");
  if (!canvas) {
    canvas = faceapi.createCanvasFromMedia(video);
    const wrapper = document.querySelector(".video-wrapper");
    if (wrapper) {
      wrapper.append(canvas);
    } else {
      document.body.append(canvas);
    }
  }

  setTimeout(() => {
    const displaySize = { width: video.clientWidth, height: video.clientHeight };
    faceapi.matchDimensions(canvas, displaySize);

    const timerId = setInterval(async () => {
      if (isRedirecting) {
        clearInterval(timerId);
        return;
      }

      const detections = await faceapi
        .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceExpressions()
        .withAgeAndGender();

      const resizedDetections = faceapi.resizeResults(detections, displaySize);
      const ctx = canvas.getContext("2d");
      
      // キャンバスをクリア
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 💡 【超重要】文字を反転させずに、描画位置だけを鏡写しにする魔法の処理
      ctx.save();
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);

      // 反転した状態の座標系で枠や点を描画する
      faceapi.draw.drawDetections(canvas, resizedDetections);
      faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
      
      // 元の座標系に戻してから文字を描画（これで文字の反転を防ぐ！）
      ctx.restore();

      resizedDetections.forEach((detection) => {
        const cameraAge = Math.round(detection.age);

        if (!isRedirecting) {
          isRedirecting = true;
          verifyAgeWithFlask(cameraAge);
        }

        // 文字だけは反転させないために、手動で反転後の位置を計算して描く
        const box = detection.detection.box;
        // 鏡写しの世界でのX座標を計算
        const flippedX = canvas.width - box.x - box.width;

        const drawBox = new faceapi.draw.DrawBox(
          { x: flippedX, y: box.y, width: box.width, height: box.height },
          { label: cameraAge + " year old " + detection.gender }
        );
        drawBox.draw(canvas);
      });
      
    }, 100);
  }, 100);
});

function verifyAgeWithFlask(cameraAge) {
  fetch('/crud/verify_age', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ camera_age: cameraAge })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === "success") {
      if (data.match) {
        alert("顔認証成功！登録年齢と一致しました。");
        location.href = data.redirect_url;
      } else {
        alert("認証失敗：登録された年齢とカメラの認識年齢が一致しません。");
        location.href = data.redirect_url;
      }
    } else {
      alert("エラー: " + data.message);
      isRedirecting = false;
    }
  })
  .catch((error) => {
    console.error('通信エラー:', error);
    isRedirecting = false;
  });
}