<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Groups</span>
        </h1>
        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button class="btn green" @click="newGroupModal= true">Create group</button>
              <Modal
                v-model="newGroupModal"
                ok-text="Create group"
                :closable="false"
                :mask-closable="false"
                @on-ok="saveGroup"
                width="400"
                title="Create group">
                <p>When you create the group, you'll be able to add users to it and configure its access.</p>
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
          </div>
        </div>
      </div>

      <div class="page-info">
        <span>
          Manage product access and roles in bulk by adding users to groups that have the required permissions.
          For example, add users to the 'administrators' group so they are able to manage other users.
        </span>
      </div>
      <div class="content-data">
        <Table :columns="columns" :data="groups" :loading="pageData.loading" @on-row-click="viewGroup"></Table>
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
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_group, this.$store.getters.getPermissions)) {
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
      newGroupModal: false,
      columns: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        }
      ],
      groups: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      search: {
        q: ''
      },
      formErrors: [],
      formData: {
        name: '',
        permissions: []
      }
    }
  },
  methods: {
    saveGroup () {
      this.api['createGroup']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Group successfully created'
        })
        this.formData.name = ''
        this.formErrors = []
        this.fetchGroups()
      }).catch((e) => {
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'error',
            text: this.formErrors.detail
          })
          this.newGroupModal = false
        } else {
          setTimeout(() => {
            this.newGroupModal = true
          }, 0)
        }
      })
    },
    fetchGroups (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        page: offset,
        q: this.search.q
      }
      this.api['userGroups']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.groups = data.results
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
      this.fetchGroups(pageNumber)
    },
    viewGroup (rowData) {
      this.$router.push({name: 'group_view', params: {slug: rowData.id}})
    }
  },
  created () {
    this.fetchGroups()
  }
}
</script>

<style scoped>

</style>
