<template>
    <div>

      <div class="bottom-header">
        <h1>
          <span class="text">Civil constructions</span>
        </h1>
        <div class="left-links">
            <div class="buttons">
              <div class="button-group m-r-5">
                <button class="btn green" @click="newCivil= true">New construction</button>
                <Modal
                  v-model="newCivil"
                  ok-text="Create"
                  width="400"
                  @on-ok="saveCivils"
                  title="Create a new construction">
                  <p>Create a new civil construction.</p>
                  <div>
                    <div>
                      <label for="assigned_to">Assign To</label>
                      <Select v-model="civilForm.assigned_to" id="assigned_to">
                        <Option v-for="item in users" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.assigned_to">{{formErrors.assigned_to[0]}}</span>
                    </div>
                    <div>
                      <label for="description">Description</label>
                      <textarea class="input" id="description" v-model="civilForm.description"></textarea>
                    </div>
                    <div>
                      <label for="civil_status">Status</label>
                      <Select v-model="civilForm.civil_status" id="civil_status">
                        <Option v-for="item in civilStatus" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.civil_status">{{formErrors.civil_status[0]}}</span>
                    </div>
                  </div>
                </Modal>
                <Modal
                  v-model="editCivil"
                  ok-text="Update"
                  width="400"
                  @on-ok="updateCivil"
                  title="Edit civil construction">
                  <p>Edit existing civil construction.</p>
                  <div>
                    <div>
                      <label for="eassigned_to">Assign To</label>
                      <Select v-model="civilForm.assigned_to" id="eassigned_to">
                        <Option v-for="item in users" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.assigned_to">{{formErrors.assigned_to[0]}}</span>
                    </div>
                    <div>
                      <label for="edescription">Description</label>
                      <textarea class="input" id="edescription" v-model="civilForm.description"></textarea>
                    </div>
                    <div>
                      <label for="ecivil_status">Status</label>
                      <Select v-model="civilForm.civil_status" id="ecivil_status">
                        <Option v-for="item in civilStatus" :value="item.value" :key="item.value">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.civil_status">{{formErrors.civil_status[0]}}</span>
                    </div>
                  </div>
                </Modal>
                <Modal
                  class="delete-group"
                  v-model="deleteCivil"
                  ok-text="Delete"
                  @on-ok="deleteCivilFunc"
                  width="400"
                  title="Delete civil construction">
                  <p>You are about to delete this civil construction. This action cannot be undone.</p>
                </Modal>
              </div>
            </div>
         </div>
      </div>

      <div class="page-info">
        <span>
          Manage constructions going on under <strong>{{projectData.name}}</strong> project.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="civils" :loading="pageData.loading"></Table>
      </div>

    </div>
</template>

<script>
export default {
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_warehouse, this.$store.getters.getPermissions)) {
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
      answerForm: {
        question: '',
        answer: ''
      },
      editCivil: false,
      clearCivil: false,
      deleteCivil: false,
      newCivil: false,
      columns: [
        {
          title: 'Assigned To',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.assigned_to.first_name + ' ' + params.row.assigned_to.last_name)
          }
        },
        {
          title: 'Assigned By',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.assigned_by.first_name + ' ' + params.row.assigned_by.last_name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.civil_status)
          }
        },
        {
          title: 'Action',
          align: 'left',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'success',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.showClear(params.index)
                  }
                }
              }, 'Clear'),
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
                    this.showEdit(params.index)
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
                    this.showDelete(params.index)
                  }
                }
              }, 'Delete')
            ])
          }
        }
      ],
      civils: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      projectSlug: this.$route.params.slug,
      users: [],
      projectData: [],
      formErrors: [],
      civilStatus: [
        {
          value: 'Active',
          label: 'Active'
        },
        {
          value: 'Complete',
          label: 'Complete'
        }
      ],
      civilForm: {
        assigned_to: '',
        description: '',
        civil_status: ''
      },
      selectedCivil: [],
      survey: [],
      questions: [],
      yesNo: [
        {
          value: 'Yes',
          label: 'Yes'
        },
        {
          value: 'No',
          label: 'No'
        }
      ]
    }
  },
  methods: {
    fetchSurvey () {
      let params = {
        type: 'Construction'
      }
      this.api['viewSurveys']('get', params, null).then(res => {
        let data = res.data
        this.survey = data.results[0]
        this.fetchQuestions()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchQuestions () {
      this.pageData.loading = true
      let params = {
        survey: this.survey.slug
      }
      this.api['viewSurveyQuestions']('get', params, null).then(res => {
        let data = res.data
        this.questions = data.results
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveAnswer () {
      this.answerForm.answered_by = this.$store.getters.getUserId
      this.api['viewSurveyQuestionAnswers']('post', null, this.answerForm).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Survey question successfully answered.'
        })
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageData.loading = false
      })
    },
    fetchCivils (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset
      }
      this.api['viewCivils']('get', params, null).then(res => {
        let data = res.data
        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.civils = data.results
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
    saveCivils () {
      this.civilForm.assigned_by = this.$store.getters.getUserId
      this.civilForm.project = this.projectData.id
      this.api['viewCivils']('post', null, this.civilForm).then(res => {
        let data = res.data
        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page
        this.civils = data.results
        this.pageData.loading = false

        this.fetchCivils()
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Construction successfully created.'
        })
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageData.loading = false
      })
    },
    paginateAction (pageNumber) {
      this.fetchCivils(pageNumber)
    },
    fetchUsers () {
      this.api['usersForm']().then(res => {
        this.users = res.data.results
        this.fetchProject()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchProject () {
      this.api['viewProject'](this.projectSlug, 'get', null, null).then(res => {
        this.projectData = res.data
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    showEdit (index) {
      this.selectedCivil = this.civils[index]
      this.civilForm.assigned_by = this.selectedCivil.assigned_by.id
      this.civilForm.assigned_to = this.selectedCivil.assigned_to.id
      this.civilForm.project = this.selectedCivil.project.id
      this.civilForm.description = this.selectedCivil.description
      this.civilForm.civil_status = this.selectedCivil.civil_status
      this.editCivil = true
    },
    showClear (index) {
      this.selectedCivil = this.civils[index]
      console.log(this.selectedCivil)
      this.$router.push({name: 'civil_survey', params: {slug: this.projectData.slug, survey_slug: this.selectedCivil.slug}})
    },
    showDelete (index) {
      this.selectedCivil = this.civils[index]
      this.deleteCivil = true
    },
    updateCivil () {
      this.civilForm.assigned_by = this.selectedCivil.assigned_by.id
      this.civilForm.project = this.selectedCivil.project.id
      this.api['viewCivil'](this.selectedCivil.slug, 'put', null, this.civilForm).then(res => {
        this.fetchCivils()
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Construction successfully updated.'
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
    deleteCivilFunc () {
      this.api['viewCivil'](this.selectedCivil.slug, 'delete', null, null).then(res => {
        this.fetchCivils()
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Construction successfully deleted.'
        })
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    }
  },
  created () {
    this.fetchCivils()
    this.fetchUsers()
    this.fetchSurvey()
  }
}
</script>

<style scoped>

</style>
