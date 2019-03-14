<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Projects</span>
        </h1>
        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button class="btn gray" @click.prevent="fetchProjects">Refresh</button>
            </div>
            <div class="button-group" v-if="this.checkPermissions.validatePermission(this.allPermissions.add_project, this.$store.getters.getPermissions)">
              <button class="btn green" @click="newProjectModal= true">Create project</button>
              <Modal
                v-model="newProjectModal"
                ok-text="Create project"
                @on-ok="saveProject"
                width="400"
                title="Create project">
                <p>When you create the project, you'll be able to add members and keep track of the progress.</p>
                <form>
                  <div>
                    <label for="name">Project's name</label>
                    <input v-model="formData.name" :required="formData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="lead">Lead</label>
                    <Select v-model="formData.lead" :class="formErrors.lead && formData.lead === '' ? 'invalid-input':''" id="lead">
                      <Option v-for="item in projectLeads" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.lead">{{formErrors.lead[0]}}</span>
                  </div>
                  <div class="display-flex m--5">
                    <div class="w50 float-left">
                      <label for="owner_name">Owner's name</label>
                      <input v-model="formData.owner_name" :required="formData.owner_name"
                             :class="formErrors.owner_name ? 'invalid-input':''"
                             class="input" type="text" value="" name="owner_name" placeholder="" id="owner_name">
                      <span class="input-help-error" v-if="formErrors.owner_name">{{formErrors.owner_name[0]}}</span>
                    </div>
                    <div class="w50 float-right">
                      <label for="owner_email">Owner's email</label>
                      <input v-model="formData.owner_email" :required="formData.owner_email"
                           :class="formErrors.owner_email ? 'invalid-input':''"
                             class="input" type="email" value="" name="owner_email" placeholder="" id="owner_email">
                      <span class="input-help-error" v-if="formErrors.owner_email">{{formErrors.owner_email[0]}}</span>
                    </div>
                  </div>
                  <div>
                    <label for="description">Description</label>
                    <textarea v-model="formData.description" :required="formData.description"
                         :class="formErrors.description ? 'invalid-input':''"
                              class="input" name="description" placeholder="" id="description"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
          </div>
        </div>
      </div>

      <div class="page-info">
        <span>
          Click on a given project to view more options like bidding, quotations, files, fabrication etc.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="projects" :loading="pageData.loading" @on-row-click="viewProject"></Table>
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
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_project, this.$store.getters.getPermissions)) {
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
      newProjectModal: false,
      columns: [
        {
          title: 'Name',
          align: 'left',
          width: 250,
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        },
        {
          title: 'Lead',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.lead.first_name + ' ' + params.row.lead.last_name)
          }
        }
      ],
      projects: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      search: {
        q: ''
      },
      projectLeads: [],
      formErrors: [],
      formData: {
        name: '',
        lead: '',
        description: '',
        owner_name: '',
        owner_email: ''
      }
    }
  },
  methods: {
    fetchProjects (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        q: this.search.q
      }
      this.api['projectsDirectory']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.projects = data.results
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
      this.fetchProjects(pageNumber)
    },
    saveProject () {
      this.api['projectsDirectory']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Project successfully created'
        })
        this.formErrors = []
        this.fetchProjects()
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
    viewProject (rowData) {
      this.$router.push({name: 'project_details', params: {slug: rowData.slug}})
    }
  },
  created () {
    this.fetchProjects(null, true)
    this.fetchLeads()
  }
}
</script>

<style scoped>

</style>
