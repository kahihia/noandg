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
          </div>
        </div>
      </div>

      <div class="page-info">
        <span>
          Click on a given project to view more options like bidding, quotations.
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
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_logisticsbid, this.$store.getters.getPermissions)) {
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
      this.$router.push({name: 'logistics_project_details', params: {slug: rowData.slug}})
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
