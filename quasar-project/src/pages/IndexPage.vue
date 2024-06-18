<template>
  <div class="q-pa-md">
    <q-card>
      <q-card-section>
        <div class="text-h6">FAQ</div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <div class="text-h6">Ważny aspekt serwera</div>
        <div class="text-h6">Aktualny adres serwera: {{ appinfo }}</div>
        <p>
          Dla tej aplikacji napisano skrypt serwera w Pythonie. Wykorzystuje on bibliotekę Flask do komunikacji z frontendem aplikacji za pomocą endpointów Axios. Serwer uruchamia się na porcie numer 5000, który powinien być dostępny dla aplikacji, aby wszystko działało poprawnie. Uprawnienia do kamery i mikrofonu są nadawane dopiero po wywołaniu prośby przyciskiem.</p>
      </q-card-section>

      <q-card-section>
        <div class="text-h6">Do czego służy ta strona?</div>
        <p>Ta strona służy do robienia zdjęć, nagrywania wideo z kamery internetowej, modyfikacji zdjęć oraz modyfikacji wideo.</p>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <div class="text-h6">Jak mogę zrobić zdjęcie?</div>
        <p>Możesz zrobić zdjęcie, przechodząc do strony "Camera" i klikając przycisk "Capture".</p>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <div class="text-h6">Jak mogę nagrać wideo?</div>
        <p>Możesz nagrać wideo, przechodząc do strony "Record Video" i klikając przycisk "Record".</p>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <div class="text-h6">Jak mogę modyfikować zdjęcia?</div>
        <p>Możesz modyfikować zdjęcia, przechodząc do strony "Show Photos" i wybierając zdjęcie do edycji.</p>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <div class="text-h6">Jak mogę modyfikować wideo?</div>
        <p>Możesz modyfikować wideo, przechodząc do strony "Show Media" i wybierając wideo do edycji.</p>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>

export default {
  data() {
    return {
      appinfo: "http://localhost:5000",
    }
  },
  mounted() {
    console.log('App info:', this.appinfo)
  }
}
</script>
