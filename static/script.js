const recordButton = document.getElementById("recordButton");
const chooseFileButton = document.getElementById("chooseFileButton");
const audioFileInput = document.getElementById("audioFileInput");
const uploadButton = document.getElementById("uploadButton");
const status = document.getElementById("status");
const audioPlayer = document.getElementById("audioPlayer");
const micClosed = document.getElementById("micClosed");
const micOpen = document.getElementById("micOpen");

let mediaRecorder;
let audioChunks = [];

// recordButton.addEventListener("click", () => {
//   if (mediaRecorder && mediaRecorder.state === "recording") {
//     mediaRecorder.stop();
//     micClosed.style.display = "inline";
//     micOpen.style.display = "none";
//   } else {
//     navigator.mediaDevices
//       .getUserMedia({ audio: true })
//       .then((stream) => {
//         mediaRecorder = new MediaRecorder(stream);

//         mediaRecorder.ondataavailable = (event) => {
//           audioChunks.push(event.data);
//         };

//         mediaRecorder.onstop = () => {
//           const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
//           const fileName = "my_recording.wav";
//           const blobWithFileName = new Blob([audioBlob], { type: audioBlob.type });
//           blobWithFileName.name = fileName;
//           const audioURL = URL.createObjectURL(blobWithFileName);

//           audioPlayer.src = audioURL;
//           audioPlayer.style.display = "block";

//           const formData = new FormData();
//           formData.append("audio", blobWithFileName);

//           fetch("/recognize-emotion", {
//             method: "POST",
//             body: formData,
//           })
//             .then((response) => response.json())
//             .then((data) => {
//               status.innerText = `Emotion: ${data.emotion}`;
//             })
//             .catch((error) => console.error(error));
//         };

//         mediaRecorder.start();
//         micClosed.style.display = "none";
//         micOpen.style.display = "inline";
//       })
//       .catch((error) => console.error(error));
//   }
// });

chooseFileButton.addEventListener("click", () => {
  audioFileInput.click();
});

audioFileInput.addEventListener("change", () => {
  if (audioFileInput.files.length > 0) {
    const selectedFileName = audioFileInput.files[0].name;
    uploadButton.style.display = "inline";
    status.innerText = `Selected File: ${selectedFileName}`;
  }
});

uploadButton.addEventListener("click", () => {
  const selectedFile = audioFileInput.files[0];
  const formData = new FormData();
  formData.append("audio", selectedFile);

  fetch('/recognize-emotion', {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      status.innerText = `Emotion: ${data.emotion}`;
    })
    .catch((error) => console.error(error));
});
