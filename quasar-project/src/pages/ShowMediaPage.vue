<template>
  <div class="row">
    <div v-if="files.length === 0" class="q-pa-lg">
      <h3>Brak plików na serwerze, jeśli chcesz coś dodać przejdź do zakładek: <router-link to="/CameraPage">zrób zdjęcie</router-link>, <router-link to="/RecordVideo">nagraj film</router-link>.</h3>
      <div class="row justify-around">
        <q-btn to="/RecordVideo" label="Record Video" />
        <q-btn to="/CameraPage" label="Camera Page" />
      </div>
    </div>
    <div class="col-6 mediaBox borderBox" v-for="file in files" :key="file">
      <video controls width="100%">
        <source :src="serverUrl + '/uploads/' + file" type="video/mp4">
        Przykro mi, twoja przeglądarka nie obsługuje wbudowanych filmów.
      </video>
      <div class="mediaBoxBottom row">
        <div class="col-12 row justify-around">
          <q-btn class="btnShowMediaBar" @click="deleteFile(file)">Usuń</q-btn>
          <q-btn class="btnShowMediaBar" @click="addWatermark(file)">Dodaj znak wodny</q-btn>
          <q-btn class="btnShowMediaBar" @click="makeBlackWhite(file)">Czarno biały</q-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      files: [],
      serverUrl: "http://localhost:5000",
    }
  },
  async created () {
    const response = await axios.get(this.serverUrl + '/files')
    this.files = response.data
  },
  methods: {
    async deleteFile(file) {
      await axios.delete(this.serverUrl + '/delete/' + file);
      const index = this.files.indexOf(file);
      if (index !== -1) {
        this.files.splice(index, 1);
      }
    },
    async addWatermark(file) {
      await axios.get(this.serverUrl + '/watermark/' + file);
      this.files.push(watermarkedFile);
      this.$set(this.watermarkOpacity, watermarkedFile, this.watermarkOpacity[file]);
    },
    async makeSepia(file) {
      await axios.get(this.serverUrl + '/sepia/' + file);
    },
    async makeBlackWhite(file) {
      await axios.get(this.serverUrl + '/blackwhite/' + file);
      const blackWhiteFile = 'blackwhite_' + file;
      this.files.push(blackWhiteFile);
    }
  }
}
</script>

