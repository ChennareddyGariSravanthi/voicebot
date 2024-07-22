document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('start-recording');
    const stopButton = document.getElementById('stop-recording');
    const responseAudio = document.getElementById('response-audio');

    let mediaRecorder;
    let audioChunks = [];

    startButton.addEventListener('click', function () {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    audioChunks = [];

                    const formData = new FormData();
                    formData.append('audio_file', audioBlob, 'recording.wav');

                    try {
                        const response = await fetch('{% url "start_streaming" %}', {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': getCsrfToken()
                            }
                        });
                        const result = await response.json();
                        if (response.ok) {
                            responseAudio.src = result.audio_url;
                        } else {
                            console.error(result.error);
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                };
                mediaRecorder.start();
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
            });
    });

    stopButton.addEventListener('click', function () {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
    });

    function getCsrfToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }
});
