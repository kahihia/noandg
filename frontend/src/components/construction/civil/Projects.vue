<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Construction</span>
        </h1>
      </div>

      <div class="page-info">
        <span>
          Manage civil construction and commissioning for different projects.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="projects" :loading="pageData.loading" @on-row-click="viewCivil"></Table>
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
      newWarehouseModal: false,
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
          title: 'Description',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.description)
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
      userGroups: [],
      formErrors: [],
      formData: {
        name: '',
        location: ''
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
    viewCivil (rowData) {
      this.$router.push({name: 'construction_project', params: {slug: rowData.slug}})
    }
  },
  created () {
    this.fetchProjects()
  }
}
</script>

<style scoped>

</style>
