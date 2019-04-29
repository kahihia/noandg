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
          <span class="text">Budget items</span>
        </h1>
      </div>
      <div class="content-data">
        <Table :columns="columnsBudget" :data="budgets" :loading="pageBudgetData.loading"></Table>
        <Page v-if="!pageBudgetData.loading && pageBudgetData.totalPages > 1" :total="pageBudgetData.totalRecords" :current="pageBudgetData.currentPage" @on-change="paginateProjectsAction" />
      </div>

      <br/>
      <div class="bottom-header">
        <h1>
          <span class="text">Equipment items</span>
        </h1>
      </div>
      <div class="content-data">
        <Table :columns="columnsEquipment" :data="equipments" :loading="pageEquipmentData.loading"></Table>
        <Page v-if="!pageEquipmentData.loading && pageEquipmentData.totalPages > 1" :total="pageEquipmentData.totalRecords" :current="pageEquipmentData.currentPage" @on-change="paginateProjectsAction" />
      </div>

      <br/>
      <div class="bottom-header">
        <h1>
          <span class="text">Project bids</span>
        </h1>
      </div>
      <div class="content-data">
        <Table :columns="columnsBids" :data="bids" :loading="pageBidsData.loading"></Table>
        <Page v-if="!pageBidsData.loading && pageBidsData.totalPages > 1" :total="pageBidsData.totalRecords" :current="pageBidsData.currentPage" @on-change="paginateProjectsAction" />
      </div>

      <br/>
      <div class="bottom-header">
        <h1>
          <span class="text">Project quotes</span>
        </h1>
      </div>
      <div class="content-data">
        <Table :columns="columnsQuotes" :data="quotes" :loading="pageQuotesData.loading"></Table>
        <Page v-if="!pageQuotesData.loading && pageQuotesData.totalPages > 1" :total="pageQuotesData.totalRecords" :current="pageQuotesData.currentPage" @on-change="paginateProjectsAction" />
      </div>
    </div>
</template>

<script>
import moment from 'moment'
export default {
  data () {
    return {
      slug: this.$route.params.slug,
      project: [],
      budgets: [],
      equipments: [],
      bids: [],
      quotes: [],
      dateRange: [],
      columnsBudget: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        },
        {
          title: 'Cost',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.unit_cost + ' ' + params.row.unit_cost_in)
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
      columnsEquipment: [
        {
          title: 'Name',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        },
        {
          title: 'Weight',
          align: 'left',
          sortable: true,
          width: 150,
          render: (h, params) => {
            return h('span', params.row.weight + ' ' + params.row.weight_in)
          }
        },
        {
          title: 'Unit cost',
          align: 'left',
          sortable: true,
          width: 150,
          render: (h, params) => {
            return h('span', params.row.unit_cost + ' ' + params.row.unit_cost_in)
          }
        },
        {
          title: 'Estimated quantity',
          align: 'left',
          sortable: true,
          width: 180,
          render: (h, params) => {
            return h('span', params.row.estimated_quantity)
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
      columnsBids: [
        {
          title: 'Vendor',
          sortable: true,
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.vendor.first_name + ' ' + params.row.vendor.last_name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.bid_status)
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
      columnsQuotes: [
        {
          title: 'Vendor',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.vendor.first_name + ' ' + params.row.vendor.last_name)
          }
        },
        {
          title: 'Equipment',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.equipment.name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.quote_status)
          }
        },
        {
          title: 'Estimated Price',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.equipment.unit_cost)
          }
        },
        {
          title: 'Quoted Price',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.quote_price)
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
        currentPage: 0
      },
      pageBudgetData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      pageEquipmentData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      pageBidsData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      pageQuotesData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      }
    }
  },
  methods: {
    filterReport (date) {
      this.dateRange = date
      this.fetchProject()
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
    fetchProject () {
      this.api['viewProject'](this.slug, 'get', null, null).then(res => {
        this.project = res.data

        this.fetchBudgets()
        this.fetchEquipments()
        this.fetchBids()
        this.fetchQuotes()
      }).catch((e) => {
        console.log(e)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchBudgets (offset) {
      this.pageBudgetData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.project.id,
        start_date: this.dateRange[0],
        end_date: this.dateRange[1]
      }
      this.api['viewBudgets']('get', params, null, null).then(res => {
        let data = res.data

        this.pageBudgetData.totalRecords = data.count
        this.pageBudgetData.totalPages = data.total_pages
        this.pageBudgetData.currentPage = data.current_page

        this.budgets = data.results
        this.pageBudgetData.loading = false
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageBudgetData.loading = false
      })
    },
    fetchEquipments (offset) {
      this.pageEquipmentData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.project.id,
        start_date: this.dateRange[0],
        end_date: this.dateRange[1]
      }
      this.api['viewEquipments']('get', params, null, null).then(res => {
        let data = res.data

        this.pageEquipmentData.totalRecords = data.count
        this.pageEquipmentData.totalPages = data.total_pages
        this.pageEquipmentData.currentPage = data.current_page

        this.equipments = data.results
        this.pageEquipmentData.loading = false
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageEquipmentData.loading = false
      })
    },
    fetchBids (offset) {
      this.pageBidsData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.project.id,
        start_date: this.dateRange[0],
        end_date: this.dateRange[1]
      }
      this.api['viewBids']('get', params, null, null).then(res => {
        let data = res.data

        this.pageBidsData.totalRecords = data.count
        this.pageBidsData.totalPages = data.total_pages
        this.pageBidsData.currentPage = data.current_page

        this.bids = data.results
        this.pageBidsData.loading = false
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageBidsData.loading = false
      })
    },
    fetchQuotes (offset) {
      this.pageQuotesData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.project.id,
        start_date: this.dateRange[0],
        end_date: this.dateRange[1]
      }
      this.api['viewQuoteItems']('get', params, null, null).then(res => {
        let data = res.data

        this.pageQuotesData.totalRecords = data.count
        this.pageQuotesData.totalPages = data.total_pages
        this.pageQuotesData.currentPage = data.current_page

        this.quotes = data.results
        this.pageQuotesData.loading = false
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageQuotesData.loading = false
      })
    },
    paginateProjectsAction (pageNumber) {
      this.fetchProjects(pageNumber)
    },
    viewProject (rowData) {
      this.$router.push({name: 'project_details', params: {slug: rowData.slug}})
    }
  },
  created () {
    this.fetchProject()
  }
}
</script>

<style scoped>

</style>
