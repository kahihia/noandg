<template>
    <div>
      <div class="bottom-header">
        <h1>
          <span class="text">Team</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectfile, this.$store.getters.getPermissions)" class="btn green" @click="newMemberModal= true">Manage team</button>
              <Modal
                v-model="newMemberModal"
                ok-text="Update team"
                @on-ok="saveProjectMember"
                width="400"
                title="Add a new user to team">
                <p>You can users to be a teamon this project on this page.</p>
                <form method="post" enctype="multipart/form-data">
                  <div>
                    <label for="member">Select user</label>
                    <Select v-model="projectForm.members" id="member" multiple>
                      <Option v-for="item in users" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.members">{{formErrors.members[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
          </div>
        </div>
      </div>

      <div class="content-data">
        <Modal
          v-model="viewFileModal"
          ok-text="Delete file"
          width="600"
          title="File preview">
          <p>You can preview and delete a given file.</p>
          <br/>
          <iframe width="565" height="400" :src="'https://docs.google.com/gview?url='+selectedFile.document+'&embedded=true'"></iframe>
        </Modal>
        <Table :columns="columns" :data="projectData.members" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      newMemberModal: false,
      viewFileModal: false,
      selectedFile: [],
      columns: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.first_name + ' ' + params.row.last_name)
          }
        },
        {
          title: 'Group',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.groups[0].name)
          }
        }
      ],
      projectData: [],
      users: [],
      selectedMember: [],
      slug: this.$route.params.slug,
      files: [],
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
        description: '',
        project: '',
        document: ''
      },
      projectForm: []
    }
  },
  methods: {
    showPreviewFile (index) {
      this.selectedFile = this.files[index]
      this.viewFileModal = true
    },
    onFileChange (e) {
      this.formData.document = this.$refs.file.files[0]
    },
    fetchProject () {
      this.api['viewProject'](this.slug, 'get', null, null).then(res => {
        this.projectData = res.data

        this.fetchFiles()
        this.fetchUsers()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })

      this.api['projectEdit'](this.slug, 'get', null, null).then(res => {
        this.projectForm = res.data
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchUsers () {
      this.api['usersForm']().then(res => {
        this.users = res.data.results
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveProjectMember () {
      this.api['projectView'](this.projectData.slug, 'put', null, this.projectForm).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project members updated'
        })
        this.formErrors = []
        this.fetchProject()
      }).catch((e) => {
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.newMemberModal = true
          }, 0)
        }
      })
    },
    paginateAction (pageNumber) {
      this.fetchFiles(pageNumber)
    },
    fetchFiles (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q
      }
      this.api['viewFiles']('get', params, null, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.files = data.results
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
    uploadFile () {
      let postData = new FormData()
      postData.append('name', this.formData.name)
      postData.append('description', this.formData.description)
      postData.append('project', this.projectData.id)
      postData.append('document', this.formData.document)
      this.api['viewFiles']('post', null, postData, true).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'File successfully uploaded'
        })
        this.formErrors = []
        this.fetchFiles()
      }).catch((e) => {
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.newMemberModal = true
          }, 0)
        }
      })
    }
  },
  created () {
    this.fetchProject()
  },
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_projectfile, this.$store.getters.getPermissions)) {
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
