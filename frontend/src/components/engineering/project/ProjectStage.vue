<template>
    <div>
      <div v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)">
        <div class="bottom-header">
          <h1>
            <span class="text">Project stages</span>
          </h1>

          <div class="left-links">
            <div class="buttons">
              <div class="button-group" v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)">
                <button class="btn gray" @click="newProjectModal= true">Update project</button>
                <Modal
                  v-model="newProjectModal"
                  ok-text="Update"
                  @on-ok="saveProject"
                  width="400"
                  title="Update project">
                  <p>Update project details.</p>
                  <form>
                    <div>
                      <label for="pname">Project's name</label>
                      <input v-model="projectData.name" :required="projectData.name"
                           :class="formErrors.name ? 'invalid-input':''"
                             class="input" type="text" value="" name="name" placeholder="" id="pname">
                      <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                    </div>
                    <div>
                      <label for="lead">Lead</label>
                      <Select v-model="projectData.lead" :class="formErrors.lead && projectData.lead === '' ? 'invalid-input':''" id="lead">
                        <Option v-for="item in projectLeads" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.lead">{{formErrors.lead[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w50 float-left">
                        <label for="owner_name">Owner's name</label>
                        <input v-model="projectData.owner_name" :required="projectData.owner_name"
                               :class="formErrors.owner_name ? 'invalid-input':''"
                               class="input" type="text" value="" name="owner_name" placeholder="" id="owner_name">
                        <span class="input-help-error" v-if="formErrors.owner_name">{{formErrors.owner_name[0]}}</span>
                      </div>
                      <div class="w50 float-right">
                        <label for="owner_email">Owner's email</label>
                        <input v-model="projectData.owner_email" :required="projectData.owner_email"
                             :class="formErrors.owner_email ? 'invalid-input':''"
                               class="input" type="email" value="" name="owner_email" placeholder="" id="owner_email">
                        <span class="input-help-error" v-if="formErrors.owner_email">{{formErrors.owner_email[0]}}</span>
                      </div>
                    </div>
                    <div>
                      <label for="description">Description</label>
                      <textarea v-model="projectData.description" :required="projectData.description"
                           :class="formErrors.description ? 'invalid-input':''"
                                class="input" name="description" placeholder="" id="description"></textarea>
                      <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                    </div>
                  </form>
                </Modal>
              </div>
              <div class="button-group" v-if="this.checkPermissions.validatePermission(this.allPermissions.delete_project, this.$store.getters.getPermissions)">
                <button class="btn red" @click="deleteProjectModal= true">Delete project</button>
                <Modal
                  class="delete-group"
                  v-model="deleteProjectModal"
                  ok-text="Delete"
                  @on-ok="deleteProject"
                  width="400"
                  title="Delete project">
                  <p>You are about to delete this project. This action cannot be undone.</p>
                </Modal>
              </div>
              <div class="button-group">
                <button v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectstage, this.$store.getters.getPermissions)" class="btn green" @click="newStage= true">Add new stage</button>
                <Modal
                  v-model="newStage"
                  ok-text="Save stage"
                  @on-ok="saveStage"
                  width="400"
                  title="Add a new project stage">
                  <form>
                    <div>
                      <label for="name">Name</label>
                      <input type="text" class="input" v-model="formData.name" id="name" />
                      <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                    </div>
                    <div>
                      <label for="percentage">Project percentage</label>
                      <input type="text" class="input" v-model="formData.stage_percentage" id="percentage" />
                      <span class="input-help-error" v-if="formErrors.stage_percentage">{{formErrors.stage_percentage[0]}}</span>
                    </div>
                  </form>
                </Modal>
              </div>
            </div>
          </div>
        </div>

        <div class="page-info">
          <p>Manage the given stages in this project and their respective completion percentages. These stages will be used for commissioning validation.</p>
        </div>

        <div class="content-data">
        <Modal
          class="delete-group"
          v-model="deleteModal"
          ok-text="Delete"
          @on-ok="deleteStage"
          width="400"
          title="Delete project stage">
          <p>You are about to delete this stage. This action cannot be undone.</p>
        </Modal>
        <Modal
          v-model="updateStageModal"
          ok-text="Confirm"
          @on-ok="updateStage"
          width="400"
          title="Update project stage">
          <p>You are about to confirm that this stage is complete.</p>
        </Modal>
        <Table :columns="columns" :data="stages" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>
        <br/><br/>
      </div>

      <div class="bottom-header">
          <h1>
            <span class="text">Project details</span>
          </h1>
      </div>

      <div class="page-info"><p>View a summary of the details and the overview of this project.</p></div>

      <Row v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)">
        <i-col span="16">
          <div class="content-data">
            <Table :columns="columnsAll" :data="stages" :loading="pageData.loading"></Table>
            <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
          </div>
        </i-col>
        <i-col span="8">
          <div id="dashboard-page">
            <h2>Project Summary</h2>
            <div class="white-box">
              <ul>
                <li>
                  <div class="tracked-te">
                    <div class="tracked-name text-ellipsis" title="dsds">Name</div>
                    <div class="tracked-project text-ellipsis has-project">
                      <span class="project-bullet" style="background:#c7741c;"></span>
                      <span class="project-name" title="Demo - Mike">{{projectData.name}}</span>
                    </div>
                  </div>
                </li>
                <li>
                  <div class="tracked-te">
                    <div class="tracked-name text-ellipsis" title="dsds">Lead</div>
                    <div class="tracked-project text-ellipsis has-project">
                      <span class="project-bullet" style="background:#c7741c;"></span>
                      <span class="project-name" title="Demo - Mike">{{projectData.lead.first_name}} {{projectData.lead.last_name}}</span>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </i-col>
      </Row>
      <div v-else style="padding: 0 20px">
        <Alert type="warning">You don't have permission to view detailed information on this page. Please use the top menu to navigate.</Alert>
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      newProjectModal: false,
      deleteProjectModal: false,
      projectLeads: [],
      newStage: false,
      updateStageModal: false,
      deleteModal: false,
      selectedFile: [],
      columns: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        },
        {
          title: 'Project percentage',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.stage_percentage)
          }
        },
        {
          title: 'Stage Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', this.filterStatus(params.row.stage_status))
          }
        },
        {
          title: 'Action',
          align: 'left',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.showDelete(params.index)
                  }
                }
              }, 'Delete'),
              h('Button', {
                props: {
                  type: 'success',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.showUpdate(params.index)
                  }
                }
              }, 'Mark complete')
            ])
          }
        }
      ],
      columnsAll: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        },
        {
          title: 'Project percentage',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.stage_percentage)
          }
        },
        {
          title: 'Stage Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', this.filterStatus(params.row.stage_status))
          }
        }
      ],
      projectData: [],
      stages: [],
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
        stage_percentage: '',
        project: ''
      },
      projectForm: [],
      selectedStage: []
    }
  },
  methods: {
    saveProject () {
      this.api['projectView'](this.projectData.slug, 'put', null, this.projectData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project successfully updated'
        })
        this.formErrors = []
        this.fetchProjects()
      }).catch((e) => {
        this.formErrors = e.response.data
        console.log(e.response)
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.newProjectModal = true
          }, 0)
        }
      })
    },
    deleteProject () {
      this.api['projectView'](this.projectData.slug, 'delete', null, null).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project successfully deleted'
        })
        this.formErrors = []
        this.$router.push({name: 'projects_directory'})
      }).catch((e) => {
        this.formErrors = e.response.data
        console.log(e.response)
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.newProjectModal = true
          }, 0)
        }
      })
    },
    fetchLeads () {
      this.api['projectLeads']().then(res => {
        this.projectLeads = res.data.results
      }).catch((e) => {
        console.log(e.response.data.detail)
      })
    },
    fetchProject () {
      this.api['projectEdit'](this.slug, 'get', null, null).then(res => {
        this.projectData = res.data
        // this.projectData.lead = this.projectData.lead.id
        this.fetchStages()
        this.fetchLeads()
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
    fetchStages () {
      let params = {
        project: this.projectData.slug
      }
      this.api['viewProjectStages']('get', params, null).then(res => {
        this.stages = res.data.results
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveStage () {
      this.formData.project = this.projectData.id
      this.api['viewProjectStages']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project stage created'
        })
        this.formErrors = []
        this.fetchProject()
      }).catch((e) => {
        this.formErrors = e.response.data
        console.log(e.response)
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.newStage = true
          }, 0)
        }
      })
    },
    updateStage () {
      this.formData.stage_status = true
      this.api['viewProjectStage'](this.selectedStage.slug, 'put', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project stage updated'
        })
        this.formErrors = []
        this.fetchProject()
      }).catch((e) => {
        this.formErrors = e.response.data
        console.log(e.response)
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.updateStage = true
          }, 0)
        }
      })
    },
    paginateAction (pageNumber) {
      this.fetchStages(pageNumber)
    },
    showDelete (index) {
      this.selectedStage = this.stages[index]
      this.deleteModal = true
    },
    showUpdate (index) {
      this.selectedStage = this.stages[index]
      this.formData = this.selectedStage
      this.updateStageModal = true
    },
    deleteStage () {
      this.api['viewProjectStage'](this.selectedStage.slug, 'delete', null, null).then(res => {
        this.fetchStages()
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Stage successfully deleted.'
        })
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    filterStatus (st) {
      if (st) {
        return 'Complete'
      } else {
        return 'Incomplete'
      }
    }
  },
  created () {
    this.fetchProject()
  },
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_project, this.$store.getters.getPermissions)) {
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
