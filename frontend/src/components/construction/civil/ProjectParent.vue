<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Project Construction</span>
        </h1>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_logisticsbid, this.$store.getters.getPermissions)" :to="{name: 'civil', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Civil</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_logisticsquote, this.$store.getters.getPermissions)||this.checkPermissions.validatePermission(this.allPermissions.view_logisticsquoteitem, this.$store.getters.getPermissions)" :to="{name: 'commissioning', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Commissioning</div>
          </div>
        </router-link>
      </div>

      <router-view/>
    </div>
</template>

<script>
export default {
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
  },
  data () {
    return {
      projectData: [],
      slug: this.$route.params.slug
    }
  },
  methods: {
    fetchProject () {
      this.api['viewProject'](this.slug, 'get', null, null).then(res => {
        this.projectData = res.data
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    }
  },
  created () {
    this.fetchProject()
  }
}
</script>

<style scoped>

</style>
