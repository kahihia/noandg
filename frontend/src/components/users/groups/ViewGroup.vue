<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">{{userGroup.name}}</span>
        </h1>
      </div>

      <div class="bottom-header">
        <h1>
          <div class="text">Groups</div>
        </h1>
        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button class="btn green" @click="editGroupModal= true">Edit name</button>
              <Modal
                v-model="editGroupModal"
                ok-text="Save changes"
                @on-ok="saveGroup"
                width="400"
                title="Edit group's name">
                <p>Edit the group's name to organize your groups better on the list.</p>
                <form>
                  <div>
                    <label for="name">Group's name</label>
                    <input v-model="formData.name" :required="formData.name"
                           :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
            <div class="button-group">
              <button class="btn gray" @click="permissionGroupModal =true">Permissions</button>
              <Modal
                v-model="permissionGroupModal"
                ok-text="Save permissions"
                @on-ok="saveGroup"
                width="600"
                title="Edit group's permissions">
                <p>Grant or deny users access to some system features by setting them to a given group.</p>
                <br/>
                <div class="permissions">
                  <Collapse>
                    <Panel class="permBox" v-for="(permission) in permissions" :key="permission.model" :name="permission.model">
                      <div class="permBoxHeading">
                        <h3>{{permission.title}}</h3>
                        <p>{{permission.summary}}</p>
                      </div>
                      <div class="permissionAllowDeny" slot="content">
                        <form class="permBoxForm" v-for="(perm, index) in permission.permissions" :key="index">
                          <div class="permInput" v-for="(model_perm, index) in perm" :key="index">
                            <input type="checkbox" v-model="permissionsCheck" :id="inputLabel(permission.model, model_perm.codename)" :value="model_perm.id">
                            <label :for="inputLabel(permission.model, model_perm.codename)" class="permInfo">{{model_perm.name}}</label>
                          </div>
                        </form>
                      </div>
                    </Panel>
                  </Collapse>
                </div>
              </Modal>
            </div>
            <div class="button-group delete-group">
              <button class="btn red" @click="deleteGroupModal= true">Delete group</button>
              <Modal
                class="delete-group"
                v-model="deleteGroupModal"
                ok-text="Delete group"
                @on-ok="deleteGroup"
                width="400"
                :title="'Delete ' + userGroup.name + '?'">
                <p>Users in this group will not be affected. Deleting a group can't be undone.</p>
              </Modal>
              <Modal
                class="delete-group"
                v-model="deleteUserModal"
                ok-text="Remove user"
                @on-ok="removeUser"
                width="400"
                title="Remove this user from this group">
                <p>You are about to remove this user from this group. You can add this user after this action.</p>
              </Modal>
            </div>
          </div>
        </div>
      </div>

      <div class="page-info">
        <dl class="d-none">
          <dt class="group-title">Group members</dt>
          <dd class="group-members">
            <span>{{pageData.totalRecords}} users found</span>
          </dd>
        </dl>
      </div>
      <div class="content-data">
        <Table :columns="userColumns" :data="users" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      editGroupModal: false,
      deleteGroupModal: false,
      permissionGroupModal: false,
      deleteUserModal: false,
      userColumns: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.first_name + ' ' + params.row.last_name)
          }
        },
        {
          title: 'Email Address',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.email)
          }
        }
      ],
      users: [],
      userGroup: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      search: {
        fq: '',
        f: ''
      },
      formErrors: [],
      formData: {
        name: '',
        permissions: []
      },
      permissions: [],
      permissionsCheck: [],
      slug: this.$route.params.slug,
      selectedUser: [],
      userForm: {}
    }
  },
  methods: {
    showDeleteStock (index) {
      this.selectedUser = this.users[index]
      this.deleteUserModal = true
    },
    fetchUsers (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        fq: this.search.fq,
        f: this.userGroup.name
      }
      this.api['usersDirectory']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.users = data.results
        this.pageData.loading = false
        console.log(this.users)
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageData.loading = false
      })
    },
    removeUser () {
      this.userForm = this.selectedUser
      this.userForm.groups = []
      console.log(this.userForm)
      this.api['viewUser'](this.selectedUser.id, 'put', null, this.userForm).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'User successfully removed'
        })
        this.formErrors = []
        this.fetchUsers()
      }).catch((e) => {
        console.log(e.response)
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.deleteUserModal = true
          }, 0)
        }
      })
    },
    paginateUsersAction (pageNumber) {
      this.fetchUsers(pageNumber)
    },
    saveGroup () {
      this.formData.permissions = this.permissionsCheck
      this.api['viewGroup'](this.slug, 'put', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Changes successfully saved'
        })
        this.formErrors = []
      }).catch((e) => {
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'error',
            text: this.formErrors.detail
          })
          this.editGroupModal = false
        } else {
          setTimeout(() => {
            this.editGroupModal = true
          }, 0)
        }
      })
    },
    deleteGroup () {
      this.api['viewGroup'](this.slug, 'delete', null, null).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Group successfully deleted'
        })
        this.$router.push({name: 'groups_directory'})
      }).catch((e) => {
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'error',
            text: this.formErrors.detail
          })
          this.deleteGroupModal = false
        } else {
          setTimeout(() => {
            this.deleteGroupModal = true
          }, 0)
        }
      })
    },
    fetchGroup () {
      this.pageData.loading = true
      this.api['viewGroup'](this.slug, 'get', null, null).then(res => {
        this.userGroup = res.data
        this.formData = res.data
        this.pageData.loading = false
        this.setCurrentPermissions(this.userGroup.permissions)
        this.fetchUsers(null, true)
        this.fetchPermissions()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageData.loading = false
      })
    },
    paginateAction (pageNumber) {
      this.fetchGroup(pageNumber)
    },
    inputLabel (model, permission) {
      return model + '' + permission
    },
    fetchPermissions () {
      this.api['groupPermissions']('get').then(res => {
        this.permissions = res.data.results
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'info',
          text: e.response.data.detail
        })
      })
    },
    setCurrentPermissions (permissions) {
      for (let i = 0; i < this.userGroup.permissions.length; i++) {
        let groupPerm = this.userGroup.permissions[i]
        this.permissionsCheck.push(groupPerm)
      }
    }
  },
  created () {
    this.fetchGroup()
  },
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_group, this.$store.getters.getPermissions)) {
      this.$notify({
        group: 'error',
        type: 'warning',
        text: 'You do not have permissions to view this page.'
      })
      this.$router.push({name: 'home'})
    }
  }
}
</script>

<style scoped>

</style>
