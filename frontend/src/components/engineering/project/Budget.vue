<template>
    <div>
      <div class="bottom-header">
        <h1>
          <span class="text">Budget & Equipments</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectequipment, this.$store.getters.getPermissions)" class="btn green" @click="newEquipmentModal= true">Create equipment</button>
              <Modal
                v-model="newEquipmentModal"
                ok-text="Create equipment"
                @on-ok="createEquipment"
                width="400"
                title="Create equipment item">
                <p>This equipment item will be assigned only to this project.</p>
                <form method="post" enctype="multipart/form-data">
                  <div>
                    <label for="name">Equipment's name</label>
                    <input v-model="equipFormData.name" :required="equipFormData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
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
                    <label for="estimated_quantity">Estimated quantity</label>
                    <input v-model="equipFormData.estimated_quantity" :required="equipFormData.estimated_quantity"
                         :class="formErrors.estimated_quantity ? 'invalid-input':''"
                           class="input" type="number" value="" name="estimated_quantity" placeholder="" id="estimated_quantity">
                    <span class="input-help-error" v-if="formErrors.estimated_quantity">{{formErrors.estimated_quantity[0]}}</span>
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
                  <div>
                    <label for="description">Description</label>
                    <textarea v-model="equipFormData.description" :required="equipFormData.description"
                         :class="formErrors.description ? 'invalid-input':''"
                              class="input" name="description" placeholder="" id="description"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
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
                v-model="deleteEquipmentModal"
                ok-text="Delete equipment item"
                @on-ok="deleteEquipment"
                width="400"
                title="Delete equipment item">
                <p>You are about to delete "<strong>{{selectedEquipment.name}}</strong>" equipment item. This action cannot be undone.</p>
              </Modal>
              <Modal
                v-model="editEquipmentModal"
                ok-text="Save changes"
                @on-ok="saveEquipment()"
                width="400"
                title="Edit equipment item">
                <form method="post" enctype="multipart/form-data">
                  <div>
                    <label for="ename">Equipment's name</label>
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
                    <label for="eestimated_quantity">Estimated quantity</label>
                    <input v-model="equipFormData.estimated_quantity" :required="equipFormData.estimated_quantity"
                         :class="formErrors.estimated_quantity ? 'invalid-input':''"
                           class="input" type="number" value="" name="estimated_quantity" placeholder="" id="eestimated_quantity">
                    <span class="input-help-error" v-if="formErrors.estimated_quantity">{{formErrors.estimated_quantity[0]}}</span>
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
                  <div>
                    <label for="edescription">Description</label>
                    <textarea v-model="equipFormData.description" :required="equipFormData.description"
                         :class="formErrors.description ? 'invalid-input':''"
                              class="input" name="description" placeholder="" id="edescription"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
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
            <div class="button-group">
              <button v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectbudget, this.$store.getters.getPermissions)" class="btn gray" @click="newBudgetModal= true">Create budget</button>
              <Modal
                v-model="newBudgetModal"
                ok-text="Create budget"
                @on-ok="createBudget"
                width="400"
                title="Create budget item">
                <p>This item will be assigned only to this project.</p>
                <form method="post" enctype="multipart/form-data">
                  <div>
                    <label for="bname">Item's name</label>
                    <input v-model="formData.name" :required="formData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="bname" placeholder="" id="bname">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div class="display-flex m--5">
                    <div class="w50 float-left">
                      <label for="bunit_cost">Unit cost</label>
                      <input v-model="formData.unit_cost" :required="formData.unit_cost"
                             :class="formErrors.unit_cost ? 'invalid-input':''"
                             class="input" type="number" value="" name="bunit_cost" placeholder="" id="bunit_cost">
                      <span class="input-help-error" v-if="formErrors.unit_cost">{{formErrors.unit_cost[0]}}</span>
                    </div>
                    <div class="w50 float-right">
                      <label for="bunit_cost_in">Unit cost currency</label>
                      <input v-model="formData.unit_cost_in" :required="formData.unit_cost_in"
                           :class="formErrors.unit_cost_in ? 'invalid-input':''"
                             class="input" type="text" value="" name="bunit_cost_in" placeholder="" id="bunit_cost_in">
                      <span class="input-help-error" v-if="formErrors.unit_cost_in">{{formErrors.unit_cost_in[0]}}</span>
                    </div>
                  </div>
                  <div>
                    <label for="bdescription">Description</label>
                    <textarea v-model="formData.description" :required="formData.description"
                         :class="formErrors.description ? 'invalid-input':''"
                              class="input" name="bdescription" placeholder="" id="bdescription"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                  </div>
                </form>
              </Modal>
              <Modal
                class="delete-group"
                v-model="deleteBudgetModal"
                ok-text="Delete budget item"
                @on-ok="deleteBudget"
                width="400"
                title="Delete budget item">
                <p>You are about to delete "<strong>{{selectedBudget.name}}</strong>" budget item. This action cannot be undone.</p>
              </Modal>
              <Modal
                v-model="editBudgetModal"
                ok-text="Save changes"
                @on-ok="saveBudget"
                width="400"
                title="Edit budget item">
                <form method="post" enctype="multipart/form-data">
                  <div>
                    <label for="ebname">Item's name</label>
                    <input v-model="selectedBudget.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="bname" placeholder="" id="ebname">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div class="display-flex m--5">
                    <div class="w50 float-left">
                      <label for="sbunit_cost">Unit cost</label>
                      <input v-model="selectedBudget.unit_cost"
                             :class="formErrors.unit_cost ? 'invalid-input':''"
                             class="input" type="number" value="" name="bunit_cost" placeholder="" id="sbunit_cost">
                      <span class="input-help-error" v-if="formErrors.unit_cost">{{formErrors.unit_cost[0]}}</span>
                    </div>
                    <div class="w50 float-right">
                      <label for="sbunit_cost_in">Unit cost currency</label>
                      <input v-model="selectedBudget.unit_cost_in"
                           :class="formErrors.unit_cost_in ? 'invalid-input':''"
                             class="input" type="text" value="" name="bunit_cost_in" placeholder="" id="sbunit_cost_in">
                      <span class="input-help-error" v-if="formErrors.unit_cost_in">{{formErrors.unit_cost_in[0]}}</span>
                    </div>
                  </div>
                  <div>
                    <label for="sbdescription">Description</label>
                    <textarea v-model="selectedBudget.description" :required="formData.description"
                         :class="formErrors.description ? 'invalid-input':''"
                              class="input" name="bdescription" placeholder="" id="sbdescription"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
          </div>
        </div>
      </div>

      <div class="content-data">

        <Tabs value="budget_items" :animated="false">
          <TabPane label="Budget items" name="budget_items">
            <Table :columns="columns" :data="budgets" :loading="pageData.loading"></Table>
            <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
          </TabPane>
          <TabPane label="Project equipments" name="budget_equipments">
            <Table :columns="equipmentColumns" :data="equipments" :loading="equipPageData.loading"></Table>
            <Page v-if="!equipPageData.loading && equipPageData.totalPages > 1" :total="equipPageData.totalRecords" :current="equipPageData.currentPage" @on-change="paginateAction" />
          </TabPane>
        </Tabs>

      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      newBudgetModal: false,
      deleteBudgetModal: false,
      editBudgetModal: false,
      newEquipmentModal: false,
      deleteEquipmentModal: false,
      editEquipmentModal: false,
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
          title: 'Cost',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.unit_cost + ' ' + params.row.unit_cost_in)
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
                    this.showEditBudget(params.index)
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
                    this.showDeleteBudget(params.index)
                  }
                }
              }, 'Delete')
            ])
          }
        }
      ],
      equipmentColumns: [
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
                    this.showDeleteEquipment(params.index)
                  }
                }
              }, 'Delete')
            ])
          }
        }
      ],
      projectData: [],
      slug: this.$route.params.slug,
      budgets: [],
      equipments: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      search: {
        q: ''
      },
      equipPageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      equipSearch: {
        q: ''
      },
      formErrors: [],
      formData: {
        name: '',
        unit_cost: '',
        unit_cost_in: '',
        description: '',
        project: ''
      },
      equipFormData: {
        project: '',
        name: '',
        unit_cost: '',
        unit_cost_in: '',
        length: '',
        width: '',
        height: '',
        measurement_in: '',
        weight: '',
        weight_in: '',
        estimated_quantity: '',
        description: ''
      },
      selectedBudget: [],
      selectedEquipment: []
    }
  },
  methods: {
    fetchProject () {
      this.api['viewProject'](this.slug, 'get', null, null).then(res => {
        this.projectData = res.data

        this.fetchBudgets()
        this.fetchEquipments()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    paginateAction (pageNumber) {
      this.fetchBudgets(pageNumber)
    },
    fetchBudgets (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q
      }
      this.api['viewBudgets']('get', params, null, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.budgets = data.results
        this.pageData.loading = false
      }).catch((e) => {
        console.log(e.response)
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.pageData.loading = false
      })
    },
    fetchEquipments (offset) {
      this.equipPageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.equipSearch.q
      }
      this.api['viewEquipments']('get', params, null, null).then(res => {
        let data = res.data

        this.equipPageData.totalRecords = data.count
        this.equipPageData.totalPages = data.total_pages
        this.equipPageData.currentPage = data.current_page

        this.equipments = data.results
        this.equipPageData.loading = false
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.equipPageData.loading = false
      })
    },
    createBudget () {
      this.formData.project = this.projectData.id
      this.api['viewBudgets']('post', null, this.formData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Budget item successfully created'
        })
        this.formErrors = []
        this.fetchBudgets()
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
            this.newBudgetModal = true
          }, 0)
        }
      })
    },
    createEquipment () {
      this.equipFormData.project = this.projectData.id
      this.api['viewEquipments']('post', null, this.equipFormData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Equipment successfully created'
        })
        this.formErrors = []
        this.fetchEquipments()
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
            this.newEquipmentModal = true
          }, 0)
        }
      })
    },
    showDeleteBudget (index) {
      this.selectedBudget = this.budgets[index]
      this.deleteBudgetModal = true
    },
    showEditBudget (index) {
      this.selectedBudget = this.budgets[index]
      this.editBudgetModal = true
    },
    deleteBudget () {
      this.api['viewBudget'](this.selectedBudget.slug, 'delete', null, null).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Budget item deleted successfully'
        })

        this.fetchBudgets()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveBudget () {
      this.selectedBudget.project = this.selectedBudget.project.id
      this.api['viewBudget'](this.selectedBudget.slug, 'put', null, this.selectedBudget).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Budget item successfully updated'
        })
        this.formErrors = []
        this.fetchBudgets()
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
    showDeleteEquipment (index) {
      this.selectedEquipment = this.equipments[index]
      this.deleteEquipmentModal = true
    },
    showEditEquipment (index) {
      this.selectedEquipment = this.equipments[index]
      this.equipFormData = this.selectedEquipment
      this.editEquipmentModal = true
    },
    deleteEquipment () {
      this.api['viewEquipment'](this.selectedEquipment.slug, 'delete', null, null).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Equipment item deleted successfully'
        })

        this.fetchEquipments()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    saveEquipment () {
      this.selectedEquipment.project = this.selectedEquipment.project.id
      this.api['viewEquipment'](this.selectedEquipment.slug, 'put', null, this.selectedEquipment).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Equipment item successfully updated'
        })
        this.formErrors = []
        this.fetchEquipments()
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
    }
  },
  created () {
    this.fetchProject()
  },
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_projectequipment, this.$store.getters.getPermissions)) {
      this.$notify({
        group: 'error',
        type: 'warning',
        text: 'You do not have permissions to view this page.'
      })
      this.$router.push({name: 'home'})
    }
  }
}
</script>

<style scoped>

</style>
