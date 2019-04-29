<template>
  <div>
    <div class="login-top"></div>
    <div class="login-content">
      <Row class="text-center">
        <i-col span="11" offset="6">
          <h1 class="login-h1">Noandg ERP</h1>
          <h2 class="login-h2">Log in to your account</h2>

          <form class="login-pane" action="" method="post" @submit.prevent="login">

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
    </div>
  </div>
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
  .login-top{
    background: #88cf8f;
    height: 370px;
  }
  .login-content{
    margin-top: -260px;
    color: #fff;
  }
  .login-h1{
    font-size: 40px;
    line-height: 1.16;
    text-align: center;
  }

  .login-h2{
    font-size: 16px;
    text-align: center;
    font-weight: 500;
    line-height: 1.52;
    margin-bottom: 0;
    padding-bottom: 25px;
    padding-top: 25px;
  }

  .login-pane{
    background-color: #fff;
    border-radius: 4px;
    padding: 48px 45px;
  }

  .login-pane label{
    display: block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .5px;
    line-height: 1.45;
    margin-bottom: 5px;
    text-transform: uppercase;
  }

  .login-pane input{
    background-color: #e3e8eb;
    border: 2px solid #e3e8eb;
    border-radius: 4px;
    box-shadow: none;
    color: #282a2d;
    display: block;
    height: 48px;
    outline: none!important;
    padding-left: 16px;
    padding-right: 16px;
    resize: none;
    transition: border-color .3s;
    width: 100%;
  }
  .login-pane button {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: baseline;
    justify-content: center;
    background-color: #e24f54;
    border: 0;
    border-radius: 24px;
    color: #fff;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    height: 48px;
    line-height: 48px;
    width: 100%;
    position: relative;
    text-align: center;
    text-decoration: none;
    text-transform: uppercase;
    -moz-osx-font-smoothing: grayscale;
    padding: 0 15px;
    margin-top: 30px;
}
</style>
