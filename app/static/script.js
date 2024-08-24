document.addEventListener('DOMContentLoaded', () => {
    const columns = {
        firstColumn: document.getElementById('firstColumn'),
        centralColumn: document.getElementById('centralColumn'),
        thirdColumn: document.getElementById('thirdColumn')
    };
    const audioFileInput = document.getElementById('audioFile');
    const selectMP3Button = document.getElementById('selectMP3');
    const useMicrophoneButton = document.getElementById('useMicrophone');
    const sensitivitySlider = document.getElementById('sensitivity');
    const sensitivityControls = document.querySelector('.controls');
    const accButton = document.getElementById('btn-acc');
    const mpiButton = document.getElementById('btn-mpi'); // Mueve esta línea aquí para evitar la redeclaración
    let audioContexts = {}; // Diccionario para mantener múltiples instancias de AudioContext
    let analysers = {};
    let sources = {};
    let isMicrophone = true;
    let sensitivity = sensitivitySlider.value;
    let isPlayingScanner = false;
    let isPlayingTurbine = false;
    let scanner;
    let turbine;
    let turbineOff;
    let music;

    function createLEDs(column) {
        for (let i = 0; i < 20; i++) {
            const led = document.createElement('div');
            led.classList.add('led');
            column.appendChild(led);
        }
    }

    createLEDs(columns.firstColumn);
    createLEDs(columns.centralColumn);
    createLEDs(columns.thirdColumn);

    sensitivitySlider.addEventListener('input', () => {
        sensitivity = sensitivitySlider.value;
        localStorage.setItem('sensitivity', sensitivity);
    });

    const savedSensitivity = localStorage.getItem('sensitivity');
    if (savedSensitivity) {
        sensitivity = savedSensitivity;
        sensitivitySlider.value = savedSensitivity;
    }

    function setupAnalyser(audioContextKey) {
        analysers[audioContextKey] = audioContexts[audioContextKey].createAnalyser();
        analysers[audioContextKey].fftSize = 32;
        analysers[audioContextKey].smoothingTimeConstant = 0.3;
    }

    function playK1Sound() {
        const audioContextKey = 'K1';
        if (audioContexts[audioContextKey]) {
            audioContexts[audioContextKey].close();
        }
        audioContexts[audioContextKey] = new (window.AudioContext || window.webkitAudioContext)();
        const audio = new Audio('../audio/K1.mp3');
        audio.crossOrigin = "anonymous";
        const track = audioContexts[audioContextKey].createMediaElementSource(audio);
        track.connect(audioContexts[audioContextKey].destination);
        audio.play();
    }

    function animateLEDs(audioContextKey) {
        const bufferLength = analysers[audioContextKey].frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        function animate() {
            analysers[audioContextKey].getByteFrequencyData(dataArray);

            const amplificationFactor = isMicrophone ? sensitivity / 2 : sensitivity / 5;

            function updateColumnLEDs(column, reducedMax) {
                const leds = column.querySelectorAll('.led');
                const half = Math.floor(leds.length / 2);

                leds.forEach((led, ledIndex) => {
                    const threshold = Math.min(
                        (Math.abs(ledIndex - half) + 1) * (255 / half),
                        (Math.abs(ledIndex - (half + 1)) + 1) * (255 / half)
                    );

                    if (reducedMax > threshold) {
                        led.classList.add('active');
                        led.style.opacity = 1;
                    } else {
                        led.classList.remove('active');
                        led.style.opacity = 0.1;
                    }
                });
            }

            const centralMax = Math.max(...dataArray);
            const centralAmplifiedMax = centralMax * amplificationFactor;
            updateColumnLEDs(columns.centralColumn, centralAmplifiedMax);

            const reducedMax = Math.max(...dataArray) * (amplificationFactor / 1.5);
            updateColumnLEDs(columns.firstColumn, reducedMax);
            updateColumnLEDs(columns.thirdColumn, reducedMax);

            requestAnimationFrame(animate);
        }

        animate();
    }

    function selectMP3() {
        playK1Sound();
        audioFileInput.click();
    }

    function sendQuestionToPrex(question) {
        playK1Sound();
        fetch('/ask_prex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        })
            .then(response => response.json())
            .then(data => {
                if (data.audio_url) {
                    playAudioAndAnimateLEDs(data.audio_url, 'prexResponse', useMicrophoneButton);
                } else {
                    alert('Error generating audio');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function playAudioAndAnimateLEDs(audioUrl, audioContextKey, button) {
        if (audioContexts[audioContextKey]) {
            audioContexts[audioContextKey].close();
        }
        audioContexts[audioContextKey] = new (window.AudioContext || window.webkitAudioContext)();
        setupAnalyser(audioContextKey);

        const audio = new Audio(audioUrl);
        audio.crossOrigin = "anonymous";
        const track = audioContexts[audioContextKey].createMediaElementSource(audio);
        track.connect(analysers[audioContextKey]);
        analysers[audioContextKey].connect(audioContexts[audioContextKey].destination);

        audio.play();
        animateLEDs(audioContextKey);

        audio.addEventListener('ended', () => {
            if (button) {
                button.classList.remove('active');
                button.classList.add('inactive');
            }
        });
    }

    useMicrophoneButton.addEventListener('click', () => {
        playK1Sound();
        try {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'es-ES';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.start();

            recognition.onresult = (event) => {
                const question = event.results[0][0].transcript;
                sendQuestionToPrex(question);
            };

            recognition.onerror = (event) => {
                console.error('Error during speech recognition:', event.error);
                alert(`Error during speech recognition: ${event.error}`);
            };

            recognition.onaudiostart = () => {
                console.log('Audio capturing started');
            };

            recognition.onaudioend = () => {
                console.log('Audio capturing ended');
            };

            recognition.onend = () => {
                console.log('Recognition service disconnected');
            };
        } catch (error) {
            console.error('Speech recognition setup error:', error);
        }
    });

    selectMP3Button.addEventListener('click', selectMP3);

    audioFileInput.addEventListener('change', function (event) {
        playK1Sound();
        const file = event.target.files[0];
        if (file) {
            const fileReader = new FileReader();
            fileReader.onload = function (e) {
                if (audioContexts['fileInput']) {
                    audioContexts['fileInput'].close();
                }
                isMicrophone = false;
                audioContexts['fileInput'] = new (window.AudioContext || window.webkitAudioContext)();
                setupAnalyser('fileInput');

                audioContexts['fileInput'].decodeAudioData(e.target.result, function (buffer) {
                    if (sources['fileInput']) {
                        sources['fileInput'].disconnect();
                    }
                    sources['fileInput'] = audioContexts['fileInput'].createBufferSource();
                    sources['fileInput'].buffer = buffer;
                    sources['fileInput'].connect(analysers['fileInput']);
                    analysers['fileInput'].connect(audioContexts['fileInput'].destination);
                    sources['fileInput'].start(0);

                    animateLEDs('fileInput');
                });
            };

            fileReader.readAsArrayBuffer(file);
        }
    });

    const radarButton = document.getElementById('btn-radar');
    radarButton.addEventListener('click', () => {
        playK1Sound();
        if (isPlayingScanner) {
            scanner.pause();
            scanner.currentTime = 0; // Reiniciar el audio al inicio
            if (audioContexts['scanner']) {
                audioContexts['scanner'].close();
            }
            isPlayingScanner = false;
        } else {
            if (audioContexts['scanner']) {
                audioContexts['scanner'].close();
            }
            audioContexts['scanner'] = new (window.AudioContext || window.webkitAudioContext)();
            setupAnalyser('scanner');

            scanner = new Audio('../audio/Scanner.wav');
            scanner.crossOrigin = "anonymous";
            scanner.loop = true; // Hacer que el audio se reproduzca en bucle

            scanner.addEventListener('canplaythrough', () => {
                console.log('Audio can play through without buffering');
                scanner.play();
            });

            scanner.addEventListener('play', () => {
                console.log('Audio is playing');
            });

            scanner.addEventListener('pause', () => {
                console.log('Audio has paused');
            });

            scanner.addEventListener('ended', () => {
                console.log('Audio has ended');
            });

            const track = audioContexts['scanner'].createMediaElementSource(scanner);
            track.connect(audioContexts['scanner'].destination);

            scanner.play();
            isPlayingScanner = true;
        }
    });

    const oil1TempButton = document.getElementById('btn-oil-temp');
    oil1TempButton.addEventListener('click', () => {
        playK1Sound();
        if (audioContexts['oilTemp']) {
            audioContexts['oilTemp'].close();
        }
        audioContexts['oilTemp'] = new (window.AudioContext || window.webkitAudioContext)();
        setupAnalyser('oilTemp');

        const oil1MP3 = new Audio('../audio/output.mp3.wav');
        oil1MP3.crossOrigin = "anonymous";
        const track = audioContexts['oilTemp'].createMediaElementSource(oil1MP3);
        track.connect(analysers['oilTemp']);
        analysers['oilTemp'].connect(audioContexts['oilTemp'].destination);

        oil1MP3.play();
        animateLEDs('oilTemp');
    });

    const fuelButton = document.getElementById('btn-fuel');
    fuelButton.addEventListener('click', () => {
        playK1Sound();
        if (isPlayingTurbine) {
            turbine.pause();
            turbine.currentTime = 0; // Reiniciar el audio de la turbina al inicio
            if (audioContexts['turbine']) {
                audioContexts['turbine'].close();
            }

            // Reproducir Turbine_off.mp3
            audioContexts['turbineOff'] = new (window.AudioContext || window.webkitAudioContext)();
            setupAnalyser('turbineOff');

            turbineOff = new Audio('../audio/Turbine_off.mp3');
            turbineOff.crossOrigin = "anonymous";

            const trackOff = audioContexts['turbineOff'].createMediaElementSource(turbineOff);
            trackOff.connect(audioContexts['turbineOff'].destination);

            turbineOff.play();
            isPlayingTurbine = false;
        } else {
            if (audioContexts['turbine']) {
                audioContexts['turbine'].close();
            }
            audioContexts['turbine'] = new (window.AudioContext || window.webkitAudioContext)();
            setupAnalyser('turbine');

            turbine = new Audio('../audio/Turbine.mp3');
            turbine.crossOrigin = "anonymous";
            turbine.loop = true; // Hacer que el audio se reproduzca en bucle

            turbine.addEventListener('canplaythrough', () => {
                console.log('Turbine audio can play through without buffering');
                turbine.play();
            });

            turbine.addEventListener('play', () => {
                console.log('Turbine audio is playing');
            });

            turbine.addEventListener('pause', () => {
                console.log('Turbine audio has paused');
            });

            turbine.addEventListener('ended', () => {
                console.log('Turbine audio has ended');
            });

            const track = audioContexts['turbine'].createMediaElementSource(turbine);
            track.connect(audioContexts['turbine'].destination);

            turbine.play();
            isPlayingTurbine = true;
        }
    });

    mpiButton.addEventListener('click', () => {
        playK1Sound();
        setTimeout(() => {
            if (audioContexts['music']) {
                audioContexts['music'].close();
            }
            audioContexts['music'] = new (window.AudioContext || window.webkitAudioContext)();
            setupAnalyser('music');

            music = new Audio('../audio/music.mp3');
            music.crossOrigin = "anonymous";

            const track = audioContexts['music'].createMediaElementSource(music);
            track.connect(audioContexts['music'].destination);

            music.play();

            music.addEventListener('ended', () => {
                mpiButton.classList.remove('active');
                mpiButton.classList.add('inactive');
            });
        }, 500); // Tiempo de espera para asegurar que K1.mp3 se reproduzca completamente
    });

    // Toggle sensitivity controls
    sensitivityControls.style.display = 'none';
    accButton.addEventListener('click', () => {
        playK1Sound();
        if (sensitivityControls.style.display === 'none') {
            sensitivityControls.style.display = 'block';
        } else {
            sensitivityControls.style.display = 'none';
        }
    });

    // Lógica para cambiar entre los modos de conducción
    const drivingModeButtons = document.querySelectorAll('.panel.center .button');
    drivingModeButtons.forEach(button => {
        playK1Sound();
        button.addEventListener('click', () => {
            playK1Sound();
            drivingModeButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            button.classList.remove('inactive');
        });
    });

    // Lógica para los otros botones
    const otherButtons = document.querySelectorAll('.panel.left .button, .panel.right .button');
    otherButtons.forEach(button => {
        playK1Sound();
        button.addEventListener('click', () => {
            playK1Sound();
            if (button.classList.contains('active')) {
                button.classList.remove('active');
                button.classList.add('inactive');
            } else {
                button.classList.add('active');
                button.classList.remove('inactive');
            }
        });
    });

    // Establecer el estado inicial
    document.getElementById('btn-normal-cruise').classList.add('active');
    document.getElementById('btn-normal-cruise').classList.remove('inactive');
});
