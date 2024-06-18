<template>
  <div class="row">
    <div class="col-6 mediaBox borderBox" v-for="file in files" :key="file">
      <img :src="serverUrl + '/uploads/' + file" width="100%">
      <div class="mediaBoxBottom row">
        <div class="col-12 row justify-around">
          <q-btn class="btnShowMediaBar" @click="deleteFile(file)">Usuń</q-btn>
          <q-btn class="btnShowMediaBar" @click="addWatermark(file)">Dodaj znak wodny</q-btn>
          <!--<q-btn class="btnShowMediaBar" @click="makeSepia(file)">Sepia</q-btn>-->
          <q-btn class="btnShowMediaBar" @click="makeBlackWhite(file)">Czarno biały</q-btn>
        </div>
        <!--<div class="col-6 boxSlider">
          <div class="row">
            <div class="col-3">
              <p style="font-size: 16px;">{{ watermarkOpacity[file] }}</p>
            </div>
            <div class="col-9" style="padding: 3px">
              <q-slider
                v-model="watermarkOpacity[file]"
                :min="0"
                :max="1"
                step="0.01"
                label="true"
                color="black"
              />
            </div>
          </div>
        </div>-->
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
    const response = await axios.get(this.serverUrl + '/photosfiles')
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
      const watermarkedFile = 'watermarked_' + file;
      this.files.push(watermarkedFile);
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

