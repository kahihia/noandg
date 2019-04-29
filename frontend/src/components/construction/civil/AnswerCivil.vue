<template>
    <div>

      <div class="bottom-header">
        <h1>
          <span class="text">Clear civil construction</span>
        </h1>
        <div class="left-links">
            <div class="buttons">
              <div class="button-group m-r-5">
                <button v-if="!surveyFilled" class="btn gray">Complete the survey first</button>
                <button v-if="surveyFilled && selectedCivil.civil_status === 'Active'" class="btn green" @click="newCivil= true">Clear construction</button>
                <button v-if="surveyFilled && selectedCivil.civil_status !== 'Active'" class="btn gray">Construction already cleared</button>
                <Modal
                  v-model="newCivil"
                  ok-text="Clear"
                  width="400"
                  @on-ok="updateCivil"
                  title="Clear construction">
                  <p>You are about to clear this construction.</p>
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
          Answer all survey questions on <strong>{{projectData.name}}</strong> project.
        </span>
      </div>

      <div class="content-data">
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
      selectedCivil: [],
      answerForm: {
        answer: ''
      },
      answerQuestion: false,
      clearCivil: false,
      deleteCivil: false,
      newCivil: false,
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
      selectedQuestion: [],
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
      ],
      surveyFilled: false
    }
  },
  methods: {
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
      this.selectedQuestion = this.questions[index]
      this.answerQuestion = true
    },
    updateCivil () {
      this.civilForm.assigned_by = this.selectedCivil.assigned_by.id
      this.civilForm.assigned_to = this.selectedCivil.assigned_to.id
      this.civilForm.project = this.selectedCivil.project.id
      this.civilForm.civil_status = 'Complete'
      this.api['viewCivil'](this.selectedCivil.slug, 'put', null, this.civilForm).then(res => {
        this.fetchCivil()
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Construction successfully updated.'
        })
      }).catch((e) => {
        console.log(e)
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
    this.fetchCivil()
    this.fetchUsers()
    this.fetchSurvey()
  }
}
</script>

<style scoped>

</style>
