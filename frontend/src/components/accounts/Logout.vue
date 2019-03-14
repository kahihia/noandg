<template>
<div></div>
</template>

<script>
export default {
  beforeCreate: function () {
    if (!this.$session.exists()) {
      this.$router.push({name: 'accounts_login'})
    }
  },
  methods: {
    logout: function () {
      this.$store.commit('setJwt', '')
      this.$store.commit('setUserId', '')
      this.$store.commit('setLoggedOut')
      this.$router.push({name: 'accounts_login'})
    }
  },
  created () {
    this.logout()
  }
}
</script>

<style scoped>

</style>
