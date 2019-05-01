<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Project</span>
        </h1>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_project, this.$store.getters.getPermissions)" :to="{name: 'project_overview', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Overview</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.add_project, this.$store.getters.getPermissions)" :to="{name: 'project_team', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Team</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_projectfile, this.$store.getters.getPermissions)" :to="{name: 'project_files', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Files</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_projectdesign, this.$store.getters.getPermissions)" :to="{name: 'project_designs', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Designs</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_projectequipment, this.$store.getters.getPermissions) || this.checkPermissions.validatePermission(this.allPermissions.view_projectbudget, this.$store.getters.getPermissions)" :to="{name: 'project_budget', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Budget & Equipments</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_projectbid, this.$store.getters.getPermissions)" :to="{name: 'project_bidding', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Bidding</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_projectquoteitem, this.$store.getters.getPermissions)" :to="{name: 'project_quotation', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Quotation</div>
          </div>
        </router-link>
        <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_projectfabrication, this.$store.getters.getPermissions)" :to="{name: 'project_fabrication', params: {'slug': slug}}" class="top-menu-links" activeClass="active">
          <div class="-text">
            <div class="-text-one">Fabrication</div>
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
