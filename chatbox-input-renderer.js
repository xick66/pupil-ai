// let chatbox = document.getElementById("chatbox");

// function submitMessage() {
//   const message = chatbox.value;
//   chatbox.value = "";

//   window.electronAPI.submitMessage("input", message);
// }

// function submitOnEnter(event) {
//   if (event.which === 13) {
//     submitMessage();
//   }
// }

// document.getElementById("chatbox").addEventListener("keydown", submitOnEnter);

// window.electronAPI.onShow(() => {
//   chatbox.focus();
// })



let chatbox = document.getElementById("chatbox");
let startVoiceButton = document.getElementById("startVoice");

function submitMessage() {
  const message = chatbox.value;
  chatbox.value = "";
  window.electronAPI.submitMessage("input", message);
}

function submitOnEnter(event) {
  if (event.which === 13) {
    submitMessage();
  }
}

document.getElementById("chatbox").addEventListener("keydown", submitOnEnter);

window.electronAPI.onShow(() => {
  chatbox.focus();
});

const recognition = new window.webkitSpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;

recognition.onaudiostart = function() {
  console.log('Audio capturing started');
};

recognition.onaudioend = function() {
  console.log('Audio capturing ended');
};

recognition.onstart = function() {
  console.log('Speech recognition service has started');
};

recognition.onend = function() {
  console.log('Speech recognition service disconnected');
};

recognition.onresult = function(event) {
  console.log('Result received');
  if (event.results.length > 0) {
    const transcript = event.results[0][0].transcript;
    console.log("Voice Input:", transcript);
    chatbox.value = transcript;
    submitMessage();
  } else {
    console.log("No speech was recognized");
  }
};

recognition.onerror = function(event) {
  console.error('Speech Recognition Error:', event.error);
};

startVoiceButton.onclick = function() {
  console.log('Starting speech recognition...');
  recognition.start();
};
