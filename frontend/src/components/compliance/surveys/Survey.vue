<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Compliance</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
            <div class="button-group">
              <button class="btn green" @click="editSurveyModal= true">Edit survey</button>
              <Modal
                v-model="editSurveyModal"
                ok-text="Update"
                @on-ok="saveSurvey"
                width="400"
                title="Edit survey">
                <p>When you create the survey, users will be required to complete it in the respective area.</p>
                <form>
                  <div>
                    <label for="name">Name</label>
                    <input v-model="survey.name" :required="survey.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="type">Type</label>
                    <Select v-model="survey.survey_type" :class="formErrors.survey_type === '' ? 'invalid-input':''" id="type">
                      <Option v-for="item in surveyTypes" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.survey_type">{{formErrors.survey_type[0]}}</span>
                  </div>
                  <div>
                    <label for="projects">Projects</label>
                    <Select v-model="survey.project" :class="formErrors.project === '' ? 'invalid-input':''" id="projects">
                      <Option v-for="item in projects" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.project">{{formErrors.project[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-header">
        <h1>
          <span class="text">Survey Questions</span>
        </h1>
        <div class="left-links">
            <div class="buttons">
              <button class="btn green" @click="newQuestionModal= true">Create question</button>
              <Modal
                v-model="newQuestionModal"
                ok-text="Create question"
                @on-ok="saveQuestion"
                width="400"
                title="Create survey question">
                <p>When you create a survey question, users will be required to answer it in the respective area.</p>
                <form>
                  <div>
                    <label for="question">Question</label>
                    <textarea v-model="formData.question" :required="formData.question"
                         :class="formErrors.question ? 'invalid-input':''"
                              class="input" name="question" placeholder="" id="question"></textarea>
                    <span class="input-help-error" v-if="formErrors.question">{{formErrors.question[0]}}</span>
                  </div>
                  <div>
                    <label for="question_type">Question Type</label>
                    <Select v-model="formData.question_type" :class="formErrors.question_type === '' ? 'invalid-input':''" id="question_type">
                      <Option v-for="item in questionTypes" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.question_type">{{formErrors.question_type[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
         </div>
      </div>

      <div class="page-info">
        <span>
          Manage different questions on this survey.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="questions" :loading="pageData.loading"></Table>
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
      editSurveyModal: false,
      newQuestionModal: false,
      columns: [
        {
          title: 'Question',
          align: 'left',
          sortable: true,
          width: 250,
          render: (h, params) => {
            return h('span', params.row.question)
          }
        },
        {
          title: 'Type',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.question_type)
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
        question: '',
        question_type: '',
        survey: ''
      },
      questionTypes: [
        {
          'value': '1',
          'label': 'Yes/No'
        },
        {
          'value': '2',
          'label': 'Numerical'
        },
        {
          'value': '3',
          'label': 'Open Ended'
        }
      ],
      surveyTypes: [
        {
          'value': 'Fabrication',
          'label': 'Fabrication'
        },
        {
          'value': 'Construction',
          'label': 'Construction'
        },
        {
          'value': 'Commissioning',
          'label': 'Commissioning'
        }
      ],
      projects: [],
      slug: this.$route.params.slug,
      survey: [],
      questions: []
    }
  },
  methods: {
    saveQuestion () {
      this.formData.survey = this.survey.id
      this.api['viewSurveyQuestions']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Survey question successfully created'
        })
        this.formErrors = []
        this.fetchQuestions()
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
            this.newQuestionModal = true
          }, 0)
        }
      })
    },
    fetchSurvey () {
      let params = {}
      this.api['viewSurveyItem'](this.slug, 'get', params, null).then(res => {
        this.survey = res.data
        this.survey.project = this.survey.project.id
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchQuestions (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        survey: this.slug,
        q: this.search.q
      }
      this.api['viewSurveyQuestions']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.questions = data.results
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
      this.fetchQuestions(pageNumber)
    },
    saveSurvey () {
      this.api['viewSurveyItem'](this.slug, 'put', null, this.survey).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Survey successfully created'
        })
        this.formErrors = []
        this.fetchSurvey()
      }).catch((e) => {
        console.log(e)
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else {
          setTimeout(() => {
            this.editSurveyModal = true
          }, 0)
        }
      })
    },
    fetchProjects () {
      this.api['projectForm']().then(res => {
        this.projects = res.data.results
      }).catch((e) => {
        console.log(e.response.data.detail)
      })
    }
  },
  created () {
    this.fetchSurvey()
    this.fetchQuestions(null, true)
    this.fetchProjects()
  }
}
</script>

<style scoped>

</style>
