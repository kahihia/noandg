<template>
  <Row class="text-center">
    <i-col span="8" offset="8">
      <h1 class="hero-headline">Sign in</h1>

      <form class="card" action="" method="post" @submit.prevent="login">

        <div class="formInputContainer">
          <label for="username">Your Email</label>
          <input v-model="user.username" :required="user.username"
                 class="input" type="text" value=""
                 name="username" placeholder="Email Address"
                 id="username">
        </div>

        <div class="formInputContainer">
          <label for="user_password">Your Password</label>
          <input autocomplete="" :required="user.password" v-model="user.password"
                 class="input"
                 type="password" name="password" placeholder="Password"
                 id="user_password">
        </div>

        <div>
          <button type="submit" class="btn-blue">Sign in</button>
        </div>

      </form>
    </i-col>
  </Row>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import api from '../../api/api'

export default {
  name: 'Login',
  data: function () {
    return {
      user: {
        username: '',
        password: ''
      },
      submitting: false
    }
  },
  methods: {
    login () {
      this.submitting = true
      api['login']('post', this.user).then(res => {
        let userData = res.data.data

        // set vuex state
        this.$store.commit('setJwt', userData.token)
        this.$store.commit('setUserId', userData.user_id)
        this.$store.commit('setPermissions', userData.permissions)
        this.$store.commit('setLoggedIn')

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

        this.$session.start()
        this.$session.set('jwt', userData.token)
        this.$session.set('user_id', userData.id)
        this.$session.set('username', userData.username)
        this.$session.set('full_name', userData.full_name)
        this.$session.set('user_group', userData.user_group)
        this.$session.set('permissions', userData.permissions)

        // Route to dashboard
        this.$router.push({name: 'home'})
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.non_field_errors[0]
        })
      })
      this.submitting = false
    }
  },
  beforeCreate: function () {
    if (this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'home'})
    }
  }
}
</script>

<style>
</style>
