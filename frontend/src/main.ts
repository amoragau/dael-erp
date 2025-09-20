import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify, Dialog } from 'quasar'
import quasarLang from 'quasar/lang/es'
import quasarIconSet from 'quasar/icon-set/material-icons'

import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/dist/quasar.css'

import App from './App.vue'
import router from './router/index'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: { Notify, Dialog },
  lang: quasarLang,
  iconSet: quasarIconSet,
})

app.mount('#app')