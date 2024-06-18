<template>
  <q-layout view="lHh Lpr lFf"  style=" background-color: #cccccc ">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          APEM app
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      style="background-color: #bbbbbb"

    >
      <q-list>
        <q-item-label
          header
        >
          Nawigacja
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
          style="background-color: #dddddd"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Strona Główna',
    caption: 'Dowiedz się więcej o aplikacji',
    icon: 'home',
    link: '/'
  },
  {
    title: 'Zrób zdjęcie',
    caption: 'Zrób zdjęcie za pomocą kamery internetowej',
    icon: 'photo_camera',
    link: '/CameraPage'
  },
  {
    title: 'Nagraj wideo',
    caption: 'Nagraj wideo za pomocą kamery internetowej i mikrofonu',
    icon: 'videocam',
    link: '/RecordVideo'
  },
  {
    title: 'Nagrania wideo',
    caption: 'Pokaż nagrania widoe',
    icon: 'perm_media',
    link: '/ShowMediaPage'
  },
  {
    title: 'Zdjęcia',
    caption: 'Obejrzyj zdjęcia',
    icon: 'collections',
    link: '/ShowPhotosPage'
  }
]

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
