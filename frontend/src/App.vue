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
              <div class="sidebar-link-pane hidden">
                <router-link to="/timeline" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-time"></span>
                  <div class="sidebar-link-text">
                    <span>Timeline</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane hidden">
                <router-link :to="{name: 'home'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-dashboard"></span>
                  <div class="sidebar-link-text">
                    <span>Dashboard</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_project, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'projects_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-projects"></span>
                  <div class="sidebar-link-text">
                    <span>Projects</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_logisticsbid, this.$store.getters.getPermissions)||
              this.checkPermissions.validatePermission(this.allPermissions.view_logisticsquote, this.$store.getters.getPermissions)||
              this.checkPermissions.validatePermission(this.allPermissions.view_logisticsquoteitem, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'logistics_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-logistics"></span>
                  <div class="sidebar-link-text">
                    <span>Logistics</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_survey, this.$store.getters.getPermissions) ||
                this.checkPermissions.validatePermission(this.allPermissions.view_surveyquestion, this.$store.getters.getPermissions) ||
                this.checkPermissions.validatePermission(this.allPermissions.view_surveyquestionanswer, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'surveys_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-inspection"></span>
                  <div class="sidebar-link-text">
                    <span>Compliance</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_warehouse, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'warehouses_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-warehouse"></span>
                  <div class="sidebar-link-text">
                    <span>Warehouse</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_commission, this.$store.getters.getPermissions) ||
                this.checkPermissions.validatePermission(this.allPermissions.view_civil, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'construction'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-construction"></span>
                  <div class="sidebar-link-text">
                    <span>Construction</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.add_project, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'reports'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-reports"></span>
                  <div class="sidebar-link-text">
                    <span>Reports</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-header"
               v-if="this.checkPermissions.validatePermission(this.allPermissions.view_group, this.$store.getters.getPermissions) ||
               this.checkPermissions.validatePermission(this.allPermissions.view_user, this.$store.getters.getPermissions) ||
                this.checkPermissions.validatePermission(this.allPermissions.view_helpissue, this.$store.getters.getPermissions)">
                <span>Manage</span>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_user, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'users_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-users"></span>
                  <div class="sidebar-link-text">
                    <span>Users</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_group, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'groups_directory'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-permissions"></span>
                  <div class="sidebar-link-text">
                    <span>User Groups</span>
                  </div>
                </router-link>
              </div>

              <div class="sidebar-link-pane" v-if="this.checkPermissions.validatePermission(this.allPermissions.view_helpissue, this.$store.getters.getPermissions)">
                <router-link :to="{name: 'help'}" class="sidebar-link" activeClass="active">
                  <span class="sidebar-link-icon icon-help"></span>
                  <div class="sidebar-link-text">
                    <span>Help</span>
                  </div>
                </router-link>
              </div>

            </div>
          </div>

          <div class="nav-accounts">
            <Dropdown>
              <a href="javascript:void(0)">
                <div class="names">
                  <span class="names-name">Account</span>
                  <span class="names-role">User log out</span>
                </div>
                <div class="names-icon">
                  <div class="names-icon-text">UA</div>
                </div>
              </a>
              <DropdownMenu slot="list">
                <DropdownItem>
                  <router-link :to="{name: 'accounts_logout'}">Log out</router-link>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
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
