<template>
  <div id="app">
    <notifications group="error"/>
    <notifications group="success"/>
    <div v-if="this.$store.state.loggedIn" id="app-body">
      <div id="content">
        <div class="left-nav">
          <div class="nav">
            <router-link class="logo" :to="{name: 'home'}"></router-link>
          </div>

          <div class="nav-notifs">
            <button class="nav-notifs-icon"></button>
          </div>

          <div class="sidebar-links">
            <div class="sidebar-links-pane">
              <div class="sidebar-link-pane">
                <router-link to="/timeline" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-time"></span>
                  <div class="sidebar-link-text">
                    <span>Timeline</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane">
                <router-link :to="{name: 'home'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-dashboard"></span>
                  <div class="sidebar-link-text">
                    <span>Dashboard</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane">
                <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_project, this.$store.getters.getPermissions)" :to="{name: 'projects_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-projects"></span>
                  <div class="sidebar-link-text">
                    <span>Projects</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-header">
                <span>Manage</span>
              </div>

              <div class="sidebar-link-pane">
                <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_user, this.$store.getters.getPermissions)" :to="{name: 'users_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-users"></span>
                  <div class="sidebar-link-text">
                    <span>Users</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane">
                <router-link v-if="this.checkPermissions.validatePermission(this.allPermissions.view_group, this.$store.getters.getPermissions)" :to="{name: 'groups_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-permissions"></span>
                  <div class="sidebar-link-text">
                    <span>User Groups</span>
                  </div>
                </router-link>
              </div>

            </div>
          </div>

          <div class="nav-accounts">
            <button>
              <div class="names">
                <span class="names-name">Muisume</span>
                <span class="names-role">Muisume's workspace</span>
              </div>
              <div class="names-icon">
                <div class="names-icon-text">Mu</div>
              </div>
            </button>
          </div>

        </div>
        <div class="right-pane">
          <router-view/>
        </div>
      </div>
    </div>
    <div v-else>
      <router-view/>
    </div>
  </div>
</template>

<script>
export default {
  beforeCreate: function () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
  },
  methods: {
    hideMainSidebar () {
      return !(this.$route.name === 'project_overview' ||
        this.$route.name === 'project_files' ||
        this.$route.name === 'project_budget' ||
        this.$route.name === 'project_bidding' ||
        this.$route.name === 'project_quotation' ||
        this.$route.name === 'project_fabrication')
    }
  }
}
</script>

<style>
  @import "assets/scss/app.scss";
</style>
