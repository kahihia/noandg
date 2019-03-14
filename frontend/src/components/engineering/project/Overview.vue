<template>
    <div class="content-data"></div>
</template>

<script>
export default {
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
