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
              <button class="btn green" @click="newUserModal= true">Create survey</button>
              <Modal
                v-model="newUserModal"
                ok-text="Create survey"
                @on-ok="saveUser"
                width="400"
                title="Create survey">
                <p>When you create the survey, users will be required to complete it in the respective area.</p>
                <form>
                  <div>
                    <label for="name">Name</label>
                    <input v-model="formData.name" :required="formData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="type">Type</label>
                    <Select v-model="formData.survey_type" :class="formErrors.survey_type === '' ? 'invalid-input':''" id="type">
                      <Option v-for="item in surveyTypes" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.survey_type">{{formErrors.survey_type[0]}}</span>
                  </div>
                  <div>
                    <label for="projects">Projects</label>
                    <Select v-model="formData.project" :class="formErrors.project === '' ? 'invalid-input':''" id="projects">
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

      <div class="page-info">
        <span>
          Manage different compliance surveys and questions.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="users" :loading="pageData.loading" @on-row-click="viewSurvey"></Table>
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
            return h('span', params.row.name)
          }
        },
        {
          title: 'Project',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.project.name)
          }
        },
        {
          title: 'Type',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.survey_type)
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
        name: '',
        survey_type: '',
        project: ''
      },
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
      projects: []
    }
  },
  methods: {
    fetchSurveys (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        q: this.search.q
      }
      this.api['viewSurveys']('get', params, null).then(res => {
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
      this.fetchSurveys(pageNumber)
    },
    saveUser () {
      this.formData.username = this.formData.email
      this.formData.password = this.formData.email
      this.formData.groups = [this.formData.groups]
      this.api['viewSurveys']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'User successfully created'
        })
        this.formErrors = []
        this.fetchSurveys()
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
    fetchProjects () {
      this.api['projectForm']().then(res => {
        this.projects = res.data.results
      }).catch((e) => {
        console.log(e.response.data.detail)
      })
    },
    viewSurvey (rowData) {
      this.$router.push({name: 'survey_details', params: {slug: rowData.slug}})
    }
  },
  created () {
    this.fetchSurveys(null, true)
    this.fetchProjects()
  }
}
</script>

<style scoped>

</style>
