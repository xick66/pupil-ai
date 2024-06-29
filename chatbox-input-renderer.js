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

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
retryCount=2
maxRetries=2
recognition.onerror = function(event) {
    console.error('Speech Recognition Error:', event.error);

    if (event.error === 'network') {
        console.log('Network error, attempting retry', retryCount);
        if (retryCount < maxRetries) {
            retryCount++;
            setTimeout(() => {
                recognition.start();
            }, retryInterval);
        } else {
            console.error('Max retries reached. Please check your network connection.');
        }
    }
};

recognition.onstart = function() {
    console.log('Speech recognition service has started');
};

recognition.onaudiostart = function() {
    console.log('Audio capturing started');
};

recognition.onaudioend = function() {
    console.log('Audio capturing ended');
};

recognition.start();
