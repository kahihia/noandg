<template>
    <div>
      <div class="bottom-header">
        <div class="filter-report">
          <p class="text">Filter date range</p>
          <DatePicker @on-change="filterReport" v-model="pageProjectsData.dateRange" :editable="false" type="daterange" split-panels placeholder="Select a date range" class="reports-date"></DatePicker>
        </div>
      </div>

      <br/>
      <div class="bottom-header">
        <h1>
          <span class="text">Projects Report</span>
        </h1>
      </div>
      <div class="content-data">
        <Table :columns="columns" :data="projects" :loading="pageProjectsData.loading" @on-row-click="viewProject"></Table>
        <Page v-if="!pageProjectsData.loading && pageProjectsData.totalPages > 1" :total="pageProjectsData.totalRecords" :current="pageProjectsData.currentPage" @on-change="paginateProjectsAction" />
      </div>
    </div>
</template>

<script>
import moment from 'moment'
export default {
  data () {
    return {
      projects: [],
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
          title: 'Project Lead',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.lead.first_name + ' ' + params.row.lead.last_name)
          }
        },
        {
          title: 'Project Owner',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.owner_name)
          }
        },
        {
          title: 'Commissioned',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', this.filterCommissioned(params.row.commissioned))
          }
        },
        {
          title: 'Created On',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', this.filterDate(params.row.created_at))
          }
        },
        {
          title: 'Last Update',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', this.filterDate(params.row.updated_at))
          }
        }
      ],
      pageProjectsData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0,
        dateRange: []
      }
    }
  },
  methods: {
    filterReport (date) {
      this.pageProjectsData.dateRange = date
      this.fetchProjects()
    },
    filterDate (dateToFilter) {
      return moment(String(dateToFilter)).format('MMM Do YYYY')
    },
    filterCommissioned (commissionStatus) {
      if (commissionStatus) {
        return 'Commissioned'
      } else {
        return 'Not Commissioned'
      }
    },
    fetchProjects () {
      this.pageProjectsData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        start_date: this.pageProjectsData.dateRange[0],
        end_date: this.pageProjectsData.dateRange[1]
      }
      this.api['projectsDirectory']('get', params, null).then(res => {
        let data = res.data

        this.pageProjectsData.totalRecords = data.count
        this.pageProjectsData.totalPages = data.total_pages
        this.pageProjectsData.currentPage = data.current_page

        this.projects = data.results
        this.pageProjectsData.loading = false
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageProjectsData.loading = false
      })
    },
    paginateProjectsAction (pageNumber) {
      this.fetchProjects(pageNumber)
    },
    viewProject (rowData) {
      this.$router.push({name: 'report_project', params: {slug: rowData.slug}})
    }
  },
  created () {
    this.fetchProjects()
  }
}
</script>

<style scoped>

</style>
