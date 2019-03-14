// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import axios from 'axios'
import Vue from 'vue'
import Vuex from 'vuex'
import App from './App'
import VueSession from 'vue-session'
import Notification from 'vue-notification'
import iView from 'iview'
import locale from 'iview/src/locale/lang/en-US'
// import 'iview/dist/styles/iview.css'
import router from './router'

import constants from './constants/index'
import api from './api/api'
import store from './store/index'
import checkPermissions from './constants/checkperms'
import allPermissions from './constants/permissions'

Vue.config.productionTip = false

// Vuex
Vue.use(Vuex)

// Session
let options = {
  persist: false
}
Vue.use(VueSession, options)

// Notifications
Vue.use(Notification)

// iView
Vue.use(iView, {locale})

// Global var
Vue.mixin({
  data: function () {
    return {
      constants: constants,
      api: api,
      checkPermissions: checkPermissions,
      allPermissions: allPermissions
    }
  }
})

// Filters
Vue.filter('sliceCapFirst', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase()
})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  beforeCreate () {
    // set session & auth token to req on axios
    let jwt = this.$store.getters.getJwt
    if (jwt) {
      let config = {
        headers: {
          'Authorization': 'Token ' + jwt
        }
      }

      Vue.prototype.$http = axios
      axios.defaults.xsrfHeaderName = 'X-CSRFToken'
      axios.defaults.xsrfCookieName = 'csrftoken'
      axios.defaults.headers = config.headers
    }
  },
  components: { App },
  template: '<App/>'
})
