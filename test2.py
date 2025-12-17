<!DOCTYPE html>
<html>
<head>
  <title>Live Audio Match</title>
</head>
<body>
  <button id="listenBtn">🎤 Listen</button>
  <p id="result"></p>

  <script>
    let mediaRecorder;
    let audioChunks = [];

    document.getElementById("listenBtn").addEventListener("click", async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
        const formData = new FormData();
        formData.append("file", audioBlob, "input.mp3");

        const response = await fetch("/process_audio", {
          method: "POST",
          body: formData
        });

        const data = await response.json();
        document.getElementById("result").innerText = "Match result: " + data.result;
      };

      audioChunks = [];
      mediaRecorder.start();

      // Stop recording after 15 seconds (you can adjust)
      setTimeout(() => mediaRecorder.stop(), 15000);
    });
  </script>
</body>
</html>