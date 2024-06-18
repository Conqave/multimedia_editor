
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/RecordVideo', component: () => import('pages/RecordVideoPage.vue') },
      { path: '/ShowMediaPage', component: () => import('pages/ShowMediaPage.vue') },
      { path: '/ShowPhotosPage', component: () => import('pages/ShowPhotosPage.vue') },
      { path: '/CameraPage', component: () => import('pages/CameraPage.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
