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

// 💡 ページ移動中や通信中に、何回もダイアログが重複して出るのを防ぐロックフラグ
let isRedirecting = false;

video.addEventListener("play", () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    // すでにリダイレクト・通信処理中なら、以降の顔認識をスキップ
    if (isRedirecting) return;

    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceExpressions()
      .withAgeAndGender();

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections);

    resizedDetections.forEach((detection) => {
      const cameraAge = Math.round(detection.age);

      if (!isRedirecting) {
        isRedirecting = true; // 💡 即座にロックをかける（連打防止）
        
        // Python側の年齢照合APIを呼び出す
        verifyAgeWithFlask(cameraAge);
      }

      const box = detection.detection.box;
      const drawBox = new faceapi.draw.DrawBox(box, {
        label: cameraAge + " year old " + detection.gender,
      });
      drawBox.draw(canvas);
    });
  }, 100);
});

// 💡 JavaScriptからFlaskのAPIへ年齢を送信し、結果をもらう関数
function verifyAgeWithFlask(cameraAge) {
  fetch('/crud/verify_age', {  // Blueprintのルーティングパス
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
        location.href = data.redirect_url; // 成功ページへ遷移
      } else {
        alert("認証失敗：登録された年齢とカメラの認識年齢が一致しません。");
        location.href = data.redirect_url;// 💡 失敗した場合はロックを解除してカメラ認識を再開
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