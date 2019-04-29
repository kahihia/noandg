<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">Warehouses</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
            <div class="button-group">
              <button class="btn green" @click="newWarehouseModal= true">Create warehouse</button>
              <Modal
                v-model="newWarehouseModal"
                ok-text="Create warehouse"
                @on-ok="saveWarehouse"
                width="400"
                title="Create warehouse">
                <p>Create different warehouses at different locations.</p>
                <form>
                  <div>
                    <label for="name">Name</label>
                    <input v-model="formData.name" :required="formData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="location">Location</label>
                    <input v-model="formData.location" :required="formData.location"
                         :class="formErrors.location ? 'invalid-input':''"
                           class="input" type="text" value="" name="location" placeholder="" id="location">
                    <span class="input-help-error" v-if="formErrors.location">{{formErrors.location[0]}}</span>
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
          Manage different warehouses.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="warehouses" :loading="pageData.loading" @on-row-click="viewWarehouse"></Table>
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
          title: 'Location',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.location)
          }
        }
      ],
      warehouses: [],
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
      },
      projects: []
    }
  },
  methods: {
    fetchWarehouses (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        q: this.search.q
      }
      this.api['viewWarehouses']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.warehouses = data.results
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
      this.fetchWarehouses(pageNumber)
    },
    saveWarehouse () {
      this.api['viewWarehouses']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Warehouse successfully created'
        })
        this.formErrors = []
        this.fetchWarehouses()
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
            this.newWarehouseModal = true
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
    viewWarehouse (rowData) {
      this.$router.push({name: 'warehouse_details', params: {slug: rowData.slug}})
    }
  },
  created () {
    this.fetchWarehouses(null, true)
    this.fetchProjects()
  }
}
</script>

<style scoped>

</style>
