<template>
    <div>
      <div class="top-header">
        <h1>
          <span class="text">{{warehouse.name}} - {{warehouse.location}}</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button class="btn red" @click="deleteWarehouseModal= true">Delete warehouse</button>
              <Modal
                class="delete-group"
                v-model="deleteWarehouseModal"
                ok-text="Delete"
                @on-ok="deleteWarehouse"
                width="400"
                title="Delete warehouse">
                <p>You are about to delete outlet <strong>"{{warehouse.name}}"</strong>. This action cannot be undone.</p>
              </Modal>
            </div>
            <div class="button-group">
              <button class="btn green" @click="editWarehouseModal= true">Edit warehouse</button>
              <Modal
                v-model="editWarehouseModal"
                ok-text="Update"
                @on-ok="saveWarehouse"
                width="400"
                title="Edit warehouse">
                <p>Edit warehouse details.</p>
                <form>
                  <div>
                    <label for="name">Name</label>
                    <input v-model="warehouse.name" :required="warehouse.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="location">Location</label>
                    <input v-model="warehouse.location" :required="warehouse.location"
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

      <div class="bottom-header">
        <h1>
          <span class="text">Stock items</span>
        </h1>
        <div class="left-links">
            <div class="buttons">
              <div class="button-group m-r-5">
                <button class="btn green" @click="newStockModal= true">Create item</button>
                <Modal
                  v-model="newStockModal"
                  ok-text="Create item"
                  @on-ok="saveStock"
                  width="400"
                  title="Create stock item">
                  <p>When you create a stock item, you'll be able to manage it and distribute it to different projects.</p>

                  <form>
                    <div>
                      <label for="stock_name">Name</label>
                      <input v-model="equipFormData.name" :required="equipFormData.name"
                           :class="formErrors.name ? 'invalid-input':''"
                             class="input" type="text" value="" name="name" placeholder="" id="stock_name">
                      <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w50 float-left">
                        <label for="unit_cost">Unit cost</label>
                        <input v-model="equipFormData.unit_cost" :required="equipFormData.unit_cost"
                               :class="formErrors.unit_cost ? 'invalid-input':''"
                               class="input" type="number" value="" name="unit_cost" placeholder="" id="unit_cost">
                        <span class="input-help-error" v-if="formErrors.unit_cost">{{formErrors.unit_cost[0]}}</span>
                      </div>
                      <div class="w50 float-right">
                        <label for="unit_cost_in">Unit cost currency</label>
                        <input v-model="equipFormData.unit_cost_in" :required="equipFormData.unit_cost_in"
                             :class="formErrors.unit_cost_in ? 'invalid-input':''"
                               class="input" type="text" value="" name="unit_cost_in" placeholder="" id="unit_cost_in">
                        <span class="input-help-error" v-if="formErrors.unit_cost_in">{{formErrors.unit_cost_in[0]}}</span>
                      </div>
                    </div>
                    <div>
                      <label for="estimated_quantity">Stock</label>
                      <input v-model="equipFormData.stock" :required="equipFormData.stock"
                           :class="formErrors.stock ? 'invalid-input':''"
                             class="input" type="number" value="" name="estimated_quantity" placeholder="" id="estimated_quantity">
                      <span class="input-help-error" v-if="formErrors.stock">{{formErrors.stock[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w30 float-left">
                        <label for="length">Length</label>
                        <input v-model="equipFormData.length" :required="equipFormData.length"
                               :class="formErrors.length ? 'invalid-input':''"
                               class="input" type="number" value="" name="length" placeholder="" id="length">
                        <span class="input-help-error" v-if="formErrors.length">{{formErrors.length[0]}}</span>
                      </div>
                      <div class="w30">
                        <label for="width">Width</label>
                        <input v-model="equipFormData.width" :required="equipFormData.width"
                             :class="formErrors.width ? 'invalid-input':''"
                               class="input" type="number" value="" name="width" placeholder="" id="width">
                        <span class="input-help-error" v-if="formErrors.width">{{formErrors.width[0]}}</span>
                      </div>
                      <div class="w30 float-right">
                        <label for="height">Height</label>
                        <input v-model="equipFormData.height" :required="equipFormData.height"
                               :class="formErrors.height ? 'invalid-input':''"
                               class="input" type="number" value="" name="height" placeholder="" id="height">
                        <span class="input-help-error" v-if="formErrors.height">{{formErrors.height[0]}}</span>
                      </div>
                    </div>
                    <div>
                      <label for="measurement_in">Unit of measurement</label>
                      <input v-model="equipFormData.measurement_in" :required="equipFormData.measurement_in"
                           :class="formErrors.measurement_in ? 'invalid-input':''"
                             class="input" type="text" value="" name="measurement_in" placeholder="" id="measurement_in">
                      <span class="input-help-error" v-if="formErrors.width">{{formErrors.width[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w50 float-left">
                        <label for="weight">Weight</label>
                        <input v-model="equipFormData.weight" :required="equipFormData.weight"
                               :class="formErrors.weight ? 'invalid-input':''"
                               class="input" type="number" value="" name="weight" placeholder="" id="weight">
                        <span class="input-help-error" v-if="formErrors.weight">{{formErrors.weight[0]}}</span>
                      </div>
                      <div class="w50 float-right">
                        <label for="weight_in">Weight in</label>
                        <input v-model="equipFormData.weight_in" :required="equipFormData.weight_in"
                             :class="formErrors.weight_in ? 'invalid-input':''"
                               class="input" type="text" value="" name="measurement_in" placeholder="" id="weight_in">
                        <span class="input-help-error" v-if="formErrors.weight_in">{{formErrors.weight_in[0]}}</span>
                      </div>
                    </div>
                  </form>
                </Modal>
                <Modal
                  class="delete-group"
                  v-model="deleteStockModal"
                  ok-text="Delete stock item"
                  @on-ok="deleteStock"
                  width="400"
                  title="Delete stock item">
                  <p>You are about to delete "<strong>{{selectedStock.name}}</strong>" stock item. This action cannot be undone.</p>
                </Modal>
                <Modal
                  v-model="editEquipmentModal"
                  ok-text="Save changes"
                  @on-ok="saveStockUpdate()"
                  width="400"
                  title="Edit stock item">
                  <form>
                    <div>
                      <label for="ename">Name</label>
                      <input v-model="equipFormData.name" :required="equipFormData.name"
                           :class="formErrors.name ? 'invalid-input':''"
                             class="input" type="text" value="" name="name" placeholder="" id="ename">
                      <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w50 float-left">
                        <label for="eunit_cost">Unit cost</label>
                        <input v-model="equipFormData.unit_cost" :required="equipFormData.unit_cost"
                               :class="formErrors.unit_cost ? 'invalid-input':''"
                               class="input" type="number" value="" name="unit_cost" placeholder="" id="eunit_cost">
                        <span class="input-help-error" v-if="formErrors.unit_cost">{{formErrors.unit_cost[0]}}</span>
                      </div>
                      <div class="w50 float-right">
                        <label for="eunit_cost_in">Unit cost currency</label>
                        <input v-model="equipFormData.unit_cost_in" :required="equipFormData.unit_cost_in"
                             :class="formErrors.unit_cost_in ? 'invalid-input':''"
                               class="input" type="text" value="" name="unit_cost_in" placeholder="" id="eunit_cost_in">
                        <span class="input-help-error" v-if="formErrors.unit_cost_in">{{formErrors.unit_cost_in[0]}}</span>
                      </div>
                    </div>
                    <div>
                      <label for="estock">Stock</label>
                      <input v-model="equipFormData.stock" :required="equipFormData.stock"
                           :class="formErrors.stock ? 'invalid-input':''"
                             class="input" type="number" value="" name="stock" min="0" placeholder="" id="estock">
                      <span class="input-help-error" v-if="formErrors.stock">{{formErrors.stock[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w30 float-left">
                        <label for="elength">Length</label>
                        <input v-model="equipFormData.length" :required="equipFormData.length"
                               :class="formErrors.length ? 'invalid-input':''"
                               class="input" type="number" value="" name="length" placeholder="" id="elength">
                        <span class="input-help-error" v-if="formErrors.length">{{formErrors.length[0]}}</span>
                      </div>
                      <div class="w30">
                        <label for="ewidth">Width</label>
                        <input v-model="equipFormData.width" :required="equipFormData.width"
                             :class="formErrors.width ? 'invalid-input':''"
                               class="input" type="number" value="" name="width" placeholder="" id="ewidth">
                        <span class="input-help-error" v-if="formErrors.width">{{formErrors.width[0]}}</span>
                      </div>
                      <div class="w30 float-right">
                        <label for="eheight">Height</label>
                        <input v-model="equipFormData.height" :required="equipFormData.height"
                               :class="formErrors.height ? 'invalid-input':''"
                               class="input" type="number" value="" name="height" placeholder="" id="eheight">
                        <span class="input-help-error" v-if="formErrors.height">{{formErrors.height[0]}}</span>
                      </div>
                    </div>
                    <div>
                      <label for="emeasurement_in">Unit of measurement</label>
                      <input v-model="equipFormData.measurement_in" :required="equipFormData.measurement_in"
                           :class="formErrors.measurement_in ? 'invalid-input':''"
                             class="input" type="text" value="" name="measurement_in" placeholder="" id="emeasurement_in">
                      <span class="input-help-error" v-if="formErrors.width">{{formErrors.width[0]}}</span>
                    </div>
                    <div class="display-flex m--5">
                      <div class="w50 float-left">
                        <label for="eweight">Weight</label>
                        <input v-model="equipFormData.weight" :required="equipFormData.weight"
                               :class="formErrors.weight ? 'invalid-input':''"
                               class="input" type="number" value="" name="weight" placeholder="" id="eweight">
                        <span class="input-help-error" v-if="formErrors.weight">{{formErrors.weight[0]}}</span>
                      </div>
                      <div class="w50 float-right">
                        <label for="eweight_in">Weight in</label>
                        <input v-model="equipFormData.weight_in" :required="equipFormData.weight_in"
                             :class="formErrors.weight_in ? 'invalid-input':''"
                               class="input" type="text" value="" name="measurement_in" placeholder="" id="eweight_in">
                        <span class="input-help-error" v-if="formErrors.weight_in">{{formErrors.weight_in[0]}}</span>
                      </div>
                    </div>
                  </form>
                </Modal>
              </div>
            </div>
            <div class="buttons">
              <div class="button-group">
                <button class="btn gray" @click="releaseStockModal= true">Release item</button>
                <Modal
                  v-model="releaseStockModal"
                  ok-text="Release item"
                  @on-ok="saveStockRelease"
                  width="400"
                  title="Release stock item">
                  <p>When you release a stock item, it'll be deducted from the current stock and distributed to different projects.</p>
                  <div>
                    <div>
                      <label for="project">Select a project</label>
                      <Select v-model="releaseData.project" :class="formErrors.project && releaseData.project === '' ? 'invalid-input':''" id="project">
                        <Option v-for="item in projects" :value="item.value" :key="item.id">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.lead">{{formErrors.lead[0]}}</span>
                    </div>
                    <div>
                      <label for="stock">Select a stock</label>
                      <Select v-model="releaseData.stock" :class="formErrors.stock && releaseData.stock === '' ? 'invalid-input':''" id="stock">
                        <Option v-for="item in stocksForm" :value="item.value" :key="item.id">{{ item.label }}</Option>
                      </Select>
                      <span class="input-help-error" v-if="formErrors.lead">{{formErrors.lead[0]}}</span>
                    </div>
                    <div>
                      <label for="quantity">Quantity</label>
                      <input min="1" v-model="releaseData.quantity" :required="releaseData.quantity"
                           :class="formErrors.quantity ? 'invalid-input':''"
                             class="input" type="number" value="" name="quantity" placeholder="" id="quantity">
                      <span class="input-help-error" v-if="formErrors.quantity">{{formErrors.quantity[0]}}</span>
                    </div>
                  </div>
                </Modal>
              </div>
            </div>
         </div>
      </div>

      <div class="page-info">
        <span>
          Manage stock items in this warehouse.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columns" :data="stocks" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>

      <br/><br/>

      <div class="bottom-header">
        <h1>
          <span class="text">Stock release record</span>
        </h1>
      </div>

      <div class="page-info">
        <span>
          Check a record of how stock was released to different projects.
        </span>
      </div>

      <div class="content-data">
        <Table :columns="columnRelease" :data="stockReleases" :loading="pageData.loading"></Table>
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
      stockReleases: [],
      columnRelease: [
        {
          title: 'Project',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.project.name)
          }
        },
        {
          title: 'Stock Item',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.stock.name)
          }
        },
        {
          title: 'Quantity Issued',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.quantity)
          }
        }
      ],
      releaseData: {
        project: 0,
        stock: 0,
        quantity: 1
      },
      editWarehouseModal: false,
      deleteWarehouseModal: false,
      newStockModal: false,
      editEquipmentModal: false,
      deleteStockModal: false,
      releaseStockModal: false,
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
          title: 'Stock',
          align: 'left',
          sortable: true,
          width: 180,
          render: (h, params) => {
            return h('span', params.row.stock)
          }
        },
        {
          title: 'Action',
          align: 'left',
          width: 150,
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
                    this.showEditEquipment(params.index)
                  }
                }
              }, 'Edit'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.showDeleteStock(params.index)
                  }
                }
              }, 'Delete')
            ])
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
        warehouse: ''
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
      warehouseTypes: [
        {
          'value': 'Shipping',
          'label': 'Shipping'
        }
      ],
      projects: [],
      slug: this.$route.params.slug,
      warehouse: [],
      stocks: [],
      stocksForm: [],
      equipFormData: {
        warehouse: '',
        name: '',
        unit_cost: '',
        unit_cost_in: '',
        length: '',
        width: '',
        height: '',
        measurement_in: '',
        weight: '',
        weight_in: '',
        stock: ''
      },
      selectedStock: []
    }
  },
  methods: {
    fetchStocks (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        warehouse: this.slug,
        q: this.search.q
      }
      this.api['viewStocks']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.stocks = data.results
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
    saveStock () {
      this.equipFormData.warehouse = this.warehouse.id
      this.api['viewStocks']('post', null, this.equipFormData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Stock item successfully created'
        })
        this.formErrors = []
        this.fetchStocks()
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
            this.newStockModal = true
          }, 0)
        }
      })
    },
    showDeleteStock (index) {
      this.selectedStock = this.stocks[index]
      this.deleteStockModal = true
    },
    showEditEquipment (index) {
      this.selectedStock = this.stocks[index]
      this.equipFormData = this.selectedStock
      this.editEquipmentModal = true
    },
    deleteStock () {
      this.api['viewStock'](this.selectedStock.slug, 'delete', null, null).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Stock item deleted successfully'
        })

        this.fetchStocks()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveStockUpdate () {
      this.selectedStock.warehouse = this.selectedStock.warehouse.id
      this.api['viewStock'](this.selectedStock.slug, 'put', null, this.selectedStock).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Stock item successfully updated'
        })
        this.formErrors = []
        this.fetchStocks()
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
            this.editBudgetModal = true
          }, 0)
        }
      })
    },
    fetchWarehouse () {
      let params = {}
      this.api['viewWarehouse'](this.slug, 'get', params, null).then(res => {
        this.warehouse = res.data
        this.fetchStockForm()
        this.fetchStockReleases()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    paginateAction (pageNumber) {
      this.fetchStocks(pageNumber)
    },
    saveWarehouse () {
      this.api['viewWarehouse'](this.slug, 'put', null, this.warehouse).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Warehouse successfully updated'
        })
        this.formErrors = []
        this.fetchWarehouse()
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
            this.editWarehouseModal = true
          }, 0)
        }
      })
    },
    deleteWarehouse () {
      this.api['viewWarehouse'](this.slug, 'delete', null, null).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Warehouse successfully deleted'
        })
        this.formErrors = []
        this.$router.push({name: 'warehouses_directory'})
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
            this.editWarehouseModal = true
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
    fetchStockForm () {
      let params = {
        warehouse: this.warehouse.slug
      }
      this.api['stockForm'](params).then(res => {
        this.stocksForm = res.data.results
      }).catch((e) => {
        console.log(e.response.data.detail)
      })
    },
    saveStockRelease () {
      this.releaseData.warehouse = this.warehouse.id
      this.releaseData.released_by = this.$store.getters.getUserId
      this.api['viewReleaseStocks']('post', null, this.releaseData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Warehouse stock release successfully created'
        })
        this.formErrors = []
        this.fetchWarehouse()
        this.fetchStocks()
        this.fetchStockReleases()
      }).catch((e) => {
        console.log(e.response)
        this.formErrors = e.response.data
        if (this.formErrors.detail) {
          this.$notify({
            group: 'error',
            type: 'warning',
            text: this.formErrors.detail
          })
        } else if (this.formErrors.non_field_errors) {
          this.$notify({
            group: 'error',
            type: 'error',
            text: this.formErrors.non_field_errors[0]
          })
        } else {
          setTimeout(() => {
            this.releaseStockModal = true
          }, 0)
        }
        setTimeout(() => {
          this.releaseStockModal = true
        }, 0)
      })
    },
    fetchStockReleases () {
      let params = {
        warehouse: this.warehouse.slug
      }
      console.log(params)
      this.api['viewReleaseStocks']('get', params, null).then(res => {
        // success
        this.stockReleases = res.data.results
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
            this.releaseStockModal = true
          }, 0)
        }
        setTimeout(() => {
          this.releaseStockModal = true
        }, 0)
      })
    }
  },
  created () {
    this.fetchWarehouse()
    this.fetchStocks(null, true)
    this.fetchProjects()
  }
}
</script>

<style scoped>

</style>
