<template>
  <q-page padding>
    <div class="row justify-center">
      <p class="text-h6">Zrób zdjęcie!</p>
    </div>
    <div class="row">
      <div class="col-12 text-center">
        <video autoplay width="90%" ref="videoplay"></video>
      </div>
      <div class="col-12 text-center row justify-around">
        <q-btn
          v-if="!cameraStart"
          label="Dostęp do kamery"
          color="primary"
          icon="camera"
          :disable="!enableCamera"
          @click="useCamera"
        />
        <q-btn
          v-else
          label="Zrób zdjęcie"
          color="primary"
          icon="camera"
          @click="captureImage"
        />
        <q-btn
          label="Pełny ekran"
          color="primary"
          icon="fullscreen"
          @click="openFullscreen"
        />
      </div>
      <div class="col-12 text-center">
        <canvas ref="canvas" width="250" height="250" style="display: none;"></canvas>
        <img src="" ref="imgTakePhoto" width="250" />
      </div>
      <div class="col-12 text-center">
        <canvas ref="canvas" style="display: none;"></canvas>
        <img src="" ref="imgTakePhoto" width="250" />
        <q-uploader ref="uploader" label="Upload" :url="appinfo + '/upload'" style="width: 100%;">
        </q-uploader>
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
      imageCapture: null,
      track: null,
      appinfo: "http://localhost:5000",
    };
  },
  mounted() {
    window.addEventListener('keyup', this.handleSpacebar);
    if (navigator.mediaDevices.getUserMedia) {
      this.enableCamera = true;
    }
    this.enumerateDevices();
    this.checkPermission();
    //this.notifyMe();
  },
  beforeUnmount() {
    window.removeEventListener('keyup', this.handleSpacebar);
  },
  methods: {
    enumerateDevices() {
      if (!navigator.mediaDevices?.enumerateDevices) {
        console.log("enumerateDevices() not supported.");
      } else {
        navigator.mediaDevices
          .enumerateDevices()
          .then((devices) => {
            devices.forEach((device) => {
              console.log(
                `${device.kind}: ${device.label} id = ${device.deviceId}`
              );
            });
          })
          .catch((err) => {
            console.error(`${err.name}: ${err.message}`);
          });
      }
    },
    openFullscreen() {
      const video = this.$refs.videoplay;
      if (video.requestFullscreen) {
        video.requestFullscreen();
      } else if (video.mozRequestFullScreen) { /* Firefox */
        video.mozRequestFullScreen();
      } else if (video.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        video.webkitRequestFullscreen();
      } else if (video.msRequestFullscreen) { /* IE/Edge */
        video.msRequestFullscreen();
      }
    },
    handleSpacebar(event) {
      if (event.code === 'Space') {
        this.captureImage();
      }
    },
    async checkPermission() {
      try {
        const permissionStatus = await navigator.permissions.query({ name: 'camera' });
        if (permissionStatus.state !== "granted") {
          alert("Dostęp do kamery jest zablokowany. Proszę nadać dostęp.");
        }
        console.log("Stan uprawnień kamery:", permissionStatus.state);
      } catch (error) {
        alert("Błąd podczas sprawdzania uprawnień kamery:", error);
      }
    },
    notifyMe() {
      if (!("Notification" in window)) {
        alert("Ta przeglądarka nie obsługuje powiadomień na pulpicie.");
      } else if (Notification.permission === "granted") {
        const notification = new Notification("Cześć!");
      } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then((permission) => {
          if (permission === "granted") {
            const notification = new Notification("Cześć!");
          }
        });
      }
    },
    useCamera() {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((mediaStream) => {
          this.cameraStart = true;
          const video = this.$refs.videoplay;
          video.srcObject = mediaStream;
          video.onloadedmetadata = () => {
            video.play();
            this.$refs.canvas.width = video.videoWidth;
            this.$refs.canvas.height = video.videoHeight;
          };
          this.track = mediaStream.getVideoTracks()[0];
          if ('ImageCapture' in window) {
            this.imageCapture = new ImageCapture(this.track);
          } else {
            console.error('ImageCapture nie jest obsługiwany w tej przeglądarce.');
          }
        })
        .catch((error) => console.error("Błąd podczas korzystania z kamery:", error));
    },
    captureImage() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');
      context.drawImage(this.$refs.videoplay, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/png');

      fetch(dataUrl)
        .then(res => res.blob())
        .then(blob => {
          const timestamp = new Date().getTime();
          const filename = `photo_${timestamp}.png`;

          const file = new File([blob], filename, { type: 'image/png' });

          this.$refs.uploader.addFiles([file]);
      });
    },
  },
};
</script>
