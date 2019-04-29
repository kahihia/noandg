<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Users</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
            <div class="button-group">
              <button class="btn green" @click="newUserModal= true">Create user</button>
              <Modal
                v-model="newUserModal"
                ok-text="Create user"
                @on-ok="saveUser"
                width="400"
                title="Create user">
                <p>When you create the user, you'll be able to add them to different system groups.</p>
                <form>
                  <div class="display-flex m--5">
                    <div class="w50 float-left">
                      <label for="first_name">First name</label>
                      <input v-model="formData.first_name" :required="formData.first_name"
                             :class="formErrors.first_name ? 'invalid-input':''"
                             class="input" type="text" value="" name="first_name" placeholder="" id="first_name">
                      <span class="input-help-error" v-if="formErrors.first_name">{{formErrors.first_name[0]}}</span>
                    </div>
                    <div class="w50 float-right">
                      <label for="last_name">Last name</label>
                      <input v-model="formData.last_name" :required="formData.last_name"
                           :class="formErrors.last_name ? 'invalid-input':''"
                             class="input" type="text" value="" name="last_name" placeholder="" id="last_name">
                      <span class="input-help-error" v-if="formErrors.last_name">{{formErrors.last_name[0]}}</span>
                    </div>
                  </div>
                  <div>
                    <label for="email">Email address</label>
                    <input v-model="formData.email" :required="formData.email"
                         :class="formErrors.email ? 'invalid-input':''"
                           class="input" type="email" value="" name="email" placeholder="" id="email">
                    <span class="input-help-error" v-if="formErrors.email">{{formErrors.email[0]}}</span>
                    <span class="input-help-error" v-if="formErrors.username">{{formErrors.username[0]}}</span>
                  </div>
                  <div>
                    <label for="groups">Group</label>
                    <Select v-model="formData.groups" :class="formErrors.groups && formData.groups === '' ? 'invalid-input':''" id="groups">
                      <Option v-for="item in userGroups" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.groups">{{formErrors.groups[0]}}</span>
                  </div>
                </form>
              </Modal>
              <Modal
                v-model="editUserModal"
                ok-text="Update"
                @on-ok="updateUser"
                width="400"
                title="Edit user">
                <p>Edit user details</p>
                <form>
                  <div class="display-flex m--5">
                    <div class="w50 float-left">
                      <label for="efirst_name">First name</label>
                      <input v-model="formData.first_name" :required="formData.first_name"
                             :class="formErrors.first_name ? 'invalid-input':''"
                             class="input" type="text" value="" name="first_name" placeholder="" id="efirst_name">
                      <span class="input-help-error" v-if="formErrors.first_name">{{formErrors.first_name[0]}}</span>
                    </div>
                    <div class="w50 float-right">
                      <label for="elast_name">Last name</label>
                      <input v-model="formData.last_name" :required="formData.last_name"
                           :class="formErrors.last_name ? 'invalid-input':''"
                             class="input" type="text" value="" name="last_name" placeholder="" id="elast_name">
                      <span class="input-help-error" v-if="formErrors.last_name">{{formErrors.last_name[0]}}</span>
                    </div>
                  </div>
                  <div>
                    <label for="eemail">Email address</label>
                    <input v-model="formData.email" :required="formData.email"
                         :class="formErrors.email ? 'invalid-input':''"
                           class="input" type="email" value="" name="email" placeholder="" id="eemail">
                    <span class="input-help-error" v-if="formErrors.email">{{formErrors.email[0]}}</span>
                    <span class="input-help-error" v-if="formErrors.username">{{formErrors.username[0]}}</span>
                  </div>
                  <div>
                    <label for="egroups">Group</label>
                    <Select v-model="formData.groups" :class="formErrors.groups && formData.groups === '' ? 'invalid-input':''" id="egroups">
                      <Option v-for="item in userGroups" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.groups">{{formErrors.groups[0]}}</span>
                  </div>
                </form>
              </Modal>
              <Modal
                class="delete-group"
                v-model="deleteUserModal"
                ok-text="Delete"
                @on-ok="deleteUser"
                width="400"
                title="Delete user">
                <p>You are about to delete this user. This action cannot be undone.</p>
              </Modal>
            </div>
            </div>
          </div>
        </div>
      </div>

      <div class="page-info">
        <span>
          Manage users account status and roles by adding users to handle different tasks.
          Create your team and start creating great things together.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="users" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>
    </div>
</template>

<script>
export default {
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_user, this.$store.getters.getPermissions)) {
      this.$notify({
        group: 'error',
        type: 'warning',
        text: 'You do not have permissions to view this page.'
      })
      this.$router.push({name: 'home'})
    }
  },
  data () {
    return {
      newUserModal: false,
      columns: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          width: 250,
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
        },
        {
          title: 'Group',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.groups[0].name)
          }
        },
        {
          title: 'Action',
          align: 'left',
          width: 150,
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'default',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.showEditUser(params.index)
                  }
                }
              }, 'Edit'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.showDeleteUser(params.index)
                  }
                }
              }, 'Delete')
            ])
          }
        }
      ],
      users: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      search: {
        q: ''
      },
      userGroups: [],
      formErrors: [],
      formData: {
        first_name: '',
        last_name: '',
        email: '',
        groups: [],
        username: '',
        password: ''
      },
      editUserModal: false,
      deleteUserModal: false,
      selectedUser: []
    }
  },
  methods: {
    fetchUsers (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        q: this.search.q
      }
      this.api['usersDirectory']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.users = data.results
        this.pageData.loading = false
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
      this.fetchUsers(pageNumber)
    },
    showDeleteUser (index) {
      this.selectedUser = this.users[index]
      this.deleteUserModal = true
    },
    showEditUser (index) {
      this.selectedUser = this.users[index]
      this.formData = this.selectedUser
      this.formData.groups = [this.selectedUser.groups[0].id]
      this.editUserModal = true
    },
    saveUser () {
      this.formData.username = this.formData.email
      this.formData.password = this.formData.email
      this.formData.groups = [this.formData.groups]
      console.log(this.formData)
      this.api['usersDirectory']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'User successfully created'
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
            this.newUserModal = true
          }, 0)
        }
      })
    },
    updateUser () {
      this.formData.username = this.formData.email
      this.formData.password = this.formData.email
      this.formData.groups = [this.formData.groups]
      console.log(this.formData)
      this.api['viewUser'](this.selectedUser.id, 'put', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'User successfully updated'
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
            this.editUserModal = true
          }, 0)
        }
      })
    },
    deleteUser () {
      this.api['viewUser'](this.selectedUser.id, 'delete', null, null).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'User successfully deleted'
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
    fetchGroups () {
      this.api['userGroupsForm']().then(res => {
        this.userGroups = res.data.results
      }).catch((e) => {
        console.log(e.response.data.detail)
      })
    }
  },
  created () {
    this.fetchUsers(null, true)
    this.fetchGroups()
  }
}
</script>

<style scoped>

</style>
