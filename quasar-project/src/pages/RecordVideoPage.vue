<template>
  <q-page padding>
    <div class="row justify-center q-mt-lg">
      <q-uploader ref="uploader" label="Upload" :url="'http://localhost:5000' + '/upload'" />
    </div>
    <div class="row justify-center q-mb-md">
      <p class="text-h6">Kamera</p>
    </div>
    <div class="row justify-center">
      <div class="col-12 text-center">
        <q-btn
          v-if="!cameraStart"
          label="Dostęp do kamery i mikrofonu"
          color="primary"
          icon="camera"
          :disable="!enableCamera"
          @click="useCamera"
        />
        <q-btn
          v-else-if="!recording"
          label="Rozpocznij nagrywanie"
          color="primary"
          icon="videocam"
          @click="startRecording"
        />
        <q-btn
          v-else
          label="Zakończ nagrywanie"
          color="primary"
          icon="stop"
          @click="stopRecording"
        />
        <!-- Wyświetlanie czasu nagrywania na bieżąco -->
        <div v-if="true" class="q-mt-md">
          <p>Czas nagrywania: {{ recordingTime }} sekund</p>
        </div>
      </div>
    </div>
    <div class="row justify-center q-mt-lg" style="background-color: #111111;">
      <p color="#ffffff">Widmo sygnału z mirofonu</p>
        <canvas ref="visualizer" class="visualizer"></canvas>
    </div>
    <div class="row justify-center q-mt-lg">
      <div class="col-6 text-center">
        <video autoplay width="90%" ref="videoplay"></video>
      </div>
      <div class="col-6 text-center">
        <canvas ref="canvas" style="display: none;"></canvas>
        <p v-if="recording">
          <img v-if="recording" src="../assets/giphy.gif" style="width:50%"/>
        </p>
        <video  v-if="!recording" controls width="90%" ref="videoreplay"></video>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "StronaKamera",
  data() {
    return {
      enableCamera: false,
      cameraStart: false,
      recording: false,
      mediaRecorder: null,
      chunks: [],
      audioContext: null,
      analyser: null,
      dataArray: null,
      bufferLength: null,
      recordingStartTime: null, // Dodajemy czas rozpoczęcia nagrywania
      recordingTime: 0, // Dodajemy czas nagrywania
      recordingInterval: null, // Dodajemy interwał do aktualizacji czasu nagrywania
    };
  },
  mounted() {
    if (navigator.mediaDevices.getUserMedia) {
      this.enableCamera = true;
    }
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.analyser = this.audioContext.createAnalyser();
  },
  methods: {
    useCamera() {
      if (this.audioContext.state === 'suspended') {
        this.audioContext.resume();
      }
      navigator.mediaDevices
        .getUserMedia({ video: true, audio: true })
        .then((mediaStream) => {
          this.cameraStart = true;
          this.$refs.videoplay.srcObject = mediaStream;
          this.mediaRecorder = new MediaRecorder(mediaStream);
          this.mediaRecorder.ondataavailable = (e) => {
            this.chunks.push(e.data);
          };
          this.mediaRecorder.onstop = () => {
            this.onMediaRecorderStop();
            this.chunks = [];
          };
          const audioTrack = mediaStream.getAudioTracks()[0];
          const source = this.audioContext.createMediaStreamSource(new MediaStream([audioTrack]));
          source.connect(this.analyser);
          this.analyser.fftSize = 256;
          this.bufferLength = this.analyser.frequencyBinCount;
          this.dataArray = new Uint8Array(this.bufferLength);
          this.draw();
        })
        .catch((error) => alert("Błąd podczas korzystania z kamery:", error));
    },
    startRecording() {
      if (this.mediaRecorder) {
        this.recording = true;
        this.mediaRecorder.start();
        this.recordingStartTime = Date.now(); // Zapisujemy czas rozpoczęcia nagrywania
        // Rozpoczynamy interwał do aktualizacji czasu nagrywania
        this.recordingInterval = setInterval(() => {
          this.recordingTime = ((Date.now() - this.recordingStartTime) / 1000).toFixed(2);
        }, 1000);
      }
    },
    stopRecording() {
      if (this.mediaRecorder) {
        this.recording = false;
        this.mediaRecorder.stop();
        this.onMediaRecorderStop();
        // Zatrzymujemy interwał do aktualizacji czasu nagrywania
        clearInterval(this.recordingInterval);
      }
    },
    onMediaRecorderStop() {
      const blob = new Blob(this.chunks, { type: 'video/mp4' });
      const url = URL.createObjectURL(blob);
      this.$refs.videoreplay.src = url;

      const timestamp = new Date().getTime();
      const filename = `video_${timestamp}.mp4`;

      const file = new File([blob], filename, { type: 'video/mp4' });

      if (file.size > 0) {
        this.$refs.uploader.addFiles([file]);
      }
      this.chunks = [];
      // Obliczamy czas nagrywania
      this.recordingTime = ((Date.now() - this.recordingStartTime) / 1000).toFixed(2);
    },
    draw() {
      requestAnimationFrame(this.draw);
      this.analyser.getByteFrequencyData(this.dataArray);
      const canvas = this.$refs.visualizer;
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);
      const barWidth = (width / this.bufferLength) * 2.5;
      let barHeight;
      let x = 0;
      for(let i = 0; i < this.bufferLength; i++) {
        barHeight = this.dataArray[i]/2;
        ctx.fillStyle = 'rgb(' + (barHeight+100) + ',50,50)';
        ctx.fillRect(x,height-barHeight/2,barWidth,barHeight);
        x += barWidth + 1;
      }
    },
  },
};
</script>

<style scoped>
.visualizer {
  width: 100%;
  height: 100px;
}
</style>
