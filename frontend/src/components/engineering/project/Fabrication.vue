<template>
    <div>
      <div class="bottom-header">
        <h1>
          <span class="text">Fabrication</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectfabrication, this.$store.getters.getPermissions)" class="btn green" @click="newFabricationModal= true">Add new</button>
              <Modal
                v-model="newFabricationModal"
                ok-text="Create"
                @on-ok="saveFabrication"
                width="400"
                title="Add a new fabrication item">
                <p>You can create new fabrications on this page.</p>
                <form method="post">
                  <div>
                    <label for="title">Title</label>
                    <input type="text" id="title" v-model="formData.title"/>
                    <span class="input-help-error" v-if="formErrors.title">{{formErrors.title[0]}}</span>
                  </div>
                  <div>
                    <label for="team">Assign to</label>
                    <Select v-model="formData.team" id="team">
                      <Option v-for="item in teams" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.team">{{formErrors.team[0]}}</span>
                  </div>
                  <div>
                    <label for="fabrication_status">Fabrication status</label>
                    <Select v-model="formData.fabrication_status" id="fabrication_status">
                      <Option v-for="item in fabStatus" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.fabrication_status">{{formErrors.fabrication_status[0]}}</span>
                  </div>
                  <div>
                    <label for="description">Summary</label>
                    <textarea v-model="formData.description" id="description"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                  </div>
                </form>
              </Modal>
              <Modal
                v-model="editFabricationModal"
                ok-text="Update"
                @on-ok="editFabrication"
                width="400"
                title="Edit fabrication">
                <p>Edit fabrication details</p>
                <form method="post">
                  <div>
                    <label for="etitle">Title</label>
                    <input type="text" id="etitle" v-model="formData.title"/>
                    <span class="input-help-error" v-if="formErrors.title">{{formErrors.title[0]}}</span>
                  </div>
                  <div>
                    <label for="eteam">Assign to</label>
                    <Select v-model="formData.team" id="eteam">
                      <Option v-for="item in teams" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.team">{{formErrors.team[0]}}</span>
                  </div>
                  <div>
                    <label for="feabrication_status">Fabrication status</label>
                    <Select v-model="formData.fabrication_status" id="feabrication_status">
                      <Option v-for="item in fabStatus" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.fabrication_status">{{formErrors.fabrication_status[0]}}</span>
                  </div>
                  <div>
                    <label for="edescription">Summary</label>
                    <textarea v-model="formData.description" id="edescription"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                  </div>
                </form>
              </Modal>
              <Modal
                class="delete-group"
                v-model="deleteFabricationModal"
                ok-text="Delete"
                @on-ok="deleteFabrication"
                width="400"
                title="Delete fabrication">
                <p>You are about to delete this fabrication. This action cannot be undone.</p>
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
        </Modal>
        <Table :columns="columns" :data="fabrications" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      editFabricationModal: false,
      deleteFabricationModal: false,
      newFabricationModal: false,
      viewFileModal: false,
      selectedFile: [],
      columns: [
        {
          title: 'Title',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.title)
          }
        },
        {
          title: 'Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.fabrication_status)
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
              }, 'Edit')
            ])
          }
        }
      ],
      projectData: [],
      fabrications: [],
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
        title: '',
        description: '',
        project: 0,
        fabrication_status: '',
        team: 0
      },
      teams: [],
      fabStatus: [
        {
          'value': 'Ongoing',
          'label': 'Ongoing'
        },
        {
          'value': 'Canceled',
          'label': 'Canceled'
        },
        {
          'value': 'Complete',
          'label': 'Complete'
        }
      ],
      projectForm: [],
      selectedFabrication: []
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

        this.fetchTeam()
        this.fetchFabrications()
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
    fetchTeam () {
      let params = {
        project: this.projectData.id
      }
      this.api['projectTeams'](params).then(res => {
        this.teams = res.data.results
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchFabrications (offset) {
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q
      }
      this.api['viewFabrications']('get', params, null, null).then(res => {
        this.fabrications = res.data.results
      }).catch((e) => {
        console.log(e)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveFabrication () {
      this.formData.project = this.projectData.id
      this.api['viewFabrications']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Fabrication item created'
        })
        this.formErrors = []
        this.fetchFabrications()
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
            this.newFabricationModal = true
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
            this.newFabricationModal = true
          }, 0)
        }
      })
    },
    viewFabrication (rowData) {
      this.$router.push({name: 'answer_fabrication', params: {slug: this.projectData.slug, fabrication_slug: rowData.slug}})
    },
    showDeleteUser (index) {
      this.selectedFabrication = this.fabrications[index]
      this.deleteFabricationModal = true
    },
    showEditUser (index) {
      this.selectedFabrication = this.fabrications[index]
      this.formData = this.selectedFabrication
      this.formData.team = this.selectedFabrication.team.id
      this.editFabricationModal = true
    },
    editFabrication () {
      this.formData.project = this.projectData.id
      this.api['viewFabrication'](this.selectedFabrication.slug, 'put', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Fabrication item updated'
        })
        this.formErrors = []
        this.fetchFabrications()
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
            this.newFabricationModal = true
          }, 0)
        }
      })
    },
    deleteFabrication () {
      this.api['viewFabrication'](this.selectedFabrication.slug, 'delete', null, null).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Fabrication item deleted.'
        })
        this.formErrors = []
        this.fetchFabrications()
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
            this.newFabricationModal = true
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
