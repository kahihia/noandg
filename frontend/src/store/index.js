import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    loggedIn: false,
    jwt: '',
    userId: '',
    permissions: [],
    count: 10
  },
  mutations: {
    setLoggedIn (state) {
      state.loggedIn = true
    },
    setUserId (state, userIdValue) {
      state.userId = userIdValue
    },
    setLoggedOut (state) {
      state.loggedIn = false
    },
    setJwt (state, jwtValue) {
      state.jwt = jwtValue
    },
    setPermissions (state, permissionsValue) {
      state.permissions = permissionsValue
    },
    increment (state) {
      state.count++
    }
  },
  getters: {
    getLoggedIn: state => {
      return state.loggedIn
    },
    getJwt: state => {
      return state.jwt
    },
    getUserId: state => {
      return state.userId
    },
    getPermissions: state => {
      return state.permissions
    }
  },
  ...Vuex.mapState,
  ...Vuex.mapMutations,
  ...Vuex.mapGetters([
    'getLoggedIn'
  ]),
  plugins: [
    createPersistedState()
  ]
})

export default store
