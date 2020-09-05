import Vue from 'vue'
import App from './App.vue'
import router from './router'
// vue-cookies
import VueCookies from 'vue-cookies'
// message
import messageService from 'vue-update-message'
// bootstrap
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// bootstrap-css
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueStar from 'vue-star'


Vue.component('VueStar', VueStar)
// vuecookies
Vue.use(VueCookies)
// message
Vue.use(messageService)
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
