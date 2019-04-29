<template>
    <div>

      <div class="bottom-header">
        <h1>
          <span class="text">Commissioning</span>
        </h1>
        <div class="left-links">
            <div class="buttons">
              <div class="button-group m-r-5">
                <button v-if="surveyFilled && !projectData.commissioned" class="btn green" @click="commitProject= true">Commission project</button>
                <button v-if="projectData.commissioned" class="btn gray">Project already commissioned</button>
                <Modal
                  v-model="commitProject"
                  ok-text="Clear"
                  width="400"
                  @on-ok="saveProject"
                  title="Commit project">
                  <p>You are about to commit this project to the client.</p>
                </Modal>
                <Modal
                  v-model="answerQuestion"
                  ok-text="Submit"
                  width="400"
                  @on-ok="saveAnswer"
                  title="Answer question">
                  <p>Answer the question below.</p>
                  <div>
                    <div>
                      <div>
                        <label>{{selectedQuestion.question}}</label>
                        <input min="0" v-model="answerForm.answer" v-if="selectedQuestion.question_type === '2'" class="input" type="number"/>
                        <Select v-model="answerForm.answer" v-if="selectedQuestion.question_type === '1'" class="input">
                          <Option v-for="item in yesNo" :key="item.value" :value="item.value">{{item.label}}</Option>
                        </Select>
                        <textarea v-model="answerForm.answer" v-if="selectedQuestion.question_type === '3'" class="input"></textarea>
                      </div>
                      <br/>
                    </div>
                  </div>
                </Modal>
              </div>
            </div>
         </div>
      </div>

      <div class="page-info">
        <span>
          Complete the survey before you can commission this project to the client.
        </span>
      </div>

      <div class="content-data">
        <div class="hidden">
          <label for="member">Select user</label>
          <Select v-model="projectForm.members" id="member" multiple>
            <Option v-for="item in users" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
          <span class="input-help-error" v-if="formErrors.members">{{formErrors.members[0]}}</span>
        </div>
        <Table :columns="columns" :data="questions" :loading="pageData.loading"></Table>
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
      surveyFilled: false,
      commitProject: false,
      answerQuestion: false,
      selectedCivil: [],
      selectedQuestion: [],
      projectData: [],
      questions: [],
      survey: [],
      users: [],
      answerForm: {
        answer: ''
      },
      columns: [
        {
          title: 'Question',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.question)
          }
        },
        {
          title: 'Answer ype',
          align: 'left',
          width: 200,
          sortable: true,
          render: (h, params) => {
            return h('span', this.getAnswerType(params.row.question_type))
          }
        },
        {
          title: 'Status',
          align: 'left',
          width: 150,
          sortable: true,
          render: (h, params) => {
            return h('span', this.getAnswerStatus(params.row.status))
          }
        },
        {
          title: 'Action',
          align: 'left',
          width: 200,
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
                    if (!params.row.status) {
                      this.showEdit(params.index)
                    }
                  }
                }
              }, this.getAnswerBtn(params.row.status))
            ])
          }
        }
      ],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      yesNo: [
        {
          value: 'Yes',
          label: 'Yes'
        },
        {
          value: 'No',
          label: 'No'
        }
      ],
      projectForm: [],
      formErrors: [],
      projectSlug: this.$route.params.slug
    }
  },
  methods: {
    fetchCivil () {
      this.api['viewCivils']('get', this.$route.params.survey_slug, null, null).then(res => {
        this.selectedCivil = res.data.results[0]
        this.civilForm = this.selectedCivil
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
    fetchProject () {
      this.api['projectEdit'](this.projectSlug, 'get').then(res => {
        this.projectData = res.data
        this.projectForm = res.data
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
        this.pageData.loading = false
        this.checkSurveyFilled()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageData.loading = false
      })
    },
    saveAnswer () {
      this.answerForm.answered_by = this.$store.getters.getUserId
      this.answerForm.question = this.selectedQuestion.id
      this.api['viewSurveyQuestionAnswers']('post', null, this.answerForm).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Survey question successfully answered.'
        })
        this.fetchQuestions()
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    showEdit (index) {
      this.selectedQuestion = this.questions[index]
      this.answerQuestion = true
    },
    checkSurveyFilled () {
      for (let i = 0; i < this.questions.length; i++) {
        let currentQuestion = this.questions[i]
        if (!currentQuestion.status) {
          this.surveyFilled = false
          break
        } else {
          this.surveyFilled = true
        }
      }
    },
    getAnswerBtn (answerStatus) {
      if (answerStatus) {
        return 'Answered'
      } else {
        return 'Answer'
      }
    },
    getAnswerStatus (answerStatus) {
      if (answerStatus) {
        return 'Answered'
      } else {
        return 'Not Answered'
      }
    },
    getAnswerType (answerStatus) {
      if (answerStatus === '1') {
        return 'Yes/No'
      } else if (answerStatus === '2') {
        return 'Numerical'
      } else {
        return 'Open Ended'
      }
    },
    fetchSurvey () {
      let params = {
        type: 'Commissioning'
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
    saveProject () {
      let formP = []
      this.api['projectView'](this.projectSlug, 'get', null, null).then(res => {
        formP = res.data
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
      this.projectData = formP
      this.projectForm.commissioned = true
      this.api['projectView'](this.projectSlug, 'put', null, this.projectForm).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project successfully commissioned'
        })
        this.formErrors = []
        this.fetchProject()
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
            this.commitProject = true
          }, 0)
        }
      })
    }
  },
  created () {
    this.fetchProject()
    this.fetchCivil()
    this.fetchSurvey()
  }
}
</script>

<style scoped>

</style>
