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

function updateVideo() {
  const link = document.getElementById('videoLink').value;
  const type = document.querySelector('input[name="videoType"]:checked').value;
  let embedLink = "";

  if (type === "youtube") {
      const videoId = link.split('v=')[1].split('&')[0];
      embedLink = `https://www.youtube.com/embed/${videoId}`;
  } else if (type === "drive") {
      const driveId = link.split('/d/')[1].split('/')[0];
      embedLink = `https://drive.google.com/file/d/${driveId}/preview`;
  }

  document.getElementById('videoFrame').src = embedLink;
}
