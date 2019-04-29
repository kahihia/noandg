<template>
    <div>
      <div class="bottom-header">
        <h1>
          <span class="text">Quotation</span>
        </h1>

         <div class="left-links">
            <div class="buttons">
              <div v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)" class="button-group">
                <button class="btn green" @click="projectQuotationModal= true">Request for quotation</button>
                <Modal
                  v-model="projectQuotationModal"
                  ok-text="Send request"
                  @on-ok="requestQuotation"
                  width="400"
                  title="Request for vendor quotation">
                  <p>When you request for quotation, each vendor whose bid on this project was accepted will be able to submit their quotes.</p>
                </Modal>
              </div>
              <div class="button-group">
                <button class="btn gray" @click.prevent="fetchProject">Refresh</button>
              </div>
            </div>
         </div>
      </div>

      <div class="page-info">
        <span v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectquote, this.$store.getters.getPermissions)">
          Request and manage project quotes. Click on the dropdown below to browse through all equipments and their respective quotes.
        </span>
        <span v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectquoteitem, this.$store.getters.getPermissions) && this.projectData.bidding">
          This project is open for bidding and vendors are able to submit their quoteitems.
        </span>
      </div>

      <div class="content-data" v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectquote, this.$store.getters.getPermissions)">
        <div class="pad-15">
          <div class="select-item">
            <div class="w30">
              <Select v-model="selectedEquipment" @on-change="fetchQuoteItems()" label="Select specific equipment">
                <Option v-for="item in equipments" :value="item.value" :key="item.value">{{ item.label }}</Option>
              </Select>
            </div>
          </div>
        </div>
        <Table :columns="columns" :data="quoteitems" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
        <!-- modals -->
        <Modal
          v-model="acceptQuoteModal"
          ok-text="Accept quote"
          @on-ok="updateQuoteStatus(selectedQuoteItem, 'Accepted')"
          width="400"
          title="Accept vendor quote">
          <p>Are you sure you accept this vendor's quote?</p>
        </Modal>
        <Modal
          class="delete-group"
          v-model="denyBidModal"
          ok-text="Deny bid"
          @on-ok="updateQuoteStatus(selectedBid.slug, 'Denied')"
          width="400"
          title="Deny vendor bid">
          <p>When you deny this bid, this vendor will not be able to bid on this project again or send a quote once a request for quotation is made.</p>
        </Modal>
      </div>

      <div class="m-b-20 m-l-20">
        <Row :gutter="8" v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectquoteitem, this.$store.getters.getPermissions)">
          <i-col class="content-are-one" span="16">
            <div class="content-data" v-if="quotesPageData.totalRecords > 0">

              <div class="pad-15">
                <Alert show-icon>
                  Project is open for you to submit your quotes. You can quote on the table below.
                </Alert>
                <legend>Check quote status</legend>
              </div>

              <Table :columns="quoteColumns" :data="vendorQuotes" :loading="pageData.loading"></Table>
              <Modal
                v-model="newQuoteModal"
                ok-text="Submit"
                @on-ok="submitQuote"
                width="400"
                title="Submit a quote">
                <form>
                  <div>
                    <label for="quote_price">Quoted price</label>
                    <input v-model="selectedQuoteItem.quote_price" :class="formErrors.quote_price ? 'invalid-input':''"
                           class="input" type="number" value="" name="quote_price" placeholder="" id="quote_price">
                    <span class="input-help-error" v-if="formErrors.quote_price">{{formErrors.quote_price[0]}}</span>
                  </div>
                </form>
              </Modal>
              <Modal
                v-model="equipmentInfoModal"
                ok-text="Close"
                width="400"
                title="Equipment details">
                <div>
                  <div>
                    <label for="name">Equipment's name</label>
                    <input v-model="equipFormData.name" :required="equipFormData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div class="display-flex m--5">
                    <div class="w50 float-left">
                      <label for="estimated_quantity">Estimated quantity</label>
                      <input v-model="equipFormData.estimated_quantity" :required="equipFormData.estimated_quantity"
                           :class="formErrors.estimated_quantity ? 'invalid-input':''"
                             class="input" type="number" value="" name="estimated_quantity" placeholder="" id="estimated_quantity">
                      <span class="input-help-error" v-if="formErrors.estimated_quantity">{{formErrors.estimated_quantity[0]}}</span>
                    </div>
                    <div class="w50 float-right">
                      <label for="unit_cost_in">Unit cost currency</label>
                      <input v-model="equipFormData.unit_cost_in" :required="equipFormData.unit_cost_in"
                           :class="formErrors.unit_cost_in ? 'invalid-input':''"
                             class="input" type="text" value="" name="unit_cost_in" placeholder="" id="unit_cost_in">
                      <span class="input-help-error" v-if="formErrors.unit_cost_in">{{formErrors.unit_cost_in[0]}}</span>
                    </div>
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
                </div>
              </Modal>
            </div>
          </i-col>
          <i-col span="8" v-if="bidExists || !bidExists && this.projectData.bidding" class="content-area-two">
            <div class="content-data">
              <div class="content-info">
                <div class="content-info-card">
                  <h4>What you need to know</h4>
                  <ul>
                    <li>You can submit quote per equipment</li>
                    <li>Click on <strong>Equipment name</strong> to view more details about a given equipment.</li>
                    <li>Once a quote on a given equipment is accepted, the status will be updated on the list table.</li>
                  </ul>
                </div>
              </div>
            </div>
          </i-col>
        </Row>
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      projectData: [],
      buttonText: '',
      bidExists: false,
      slug: this.$route.params.slug,
      projectQuotationModal: false,
      newBidModal: false,
      newQuoteModal: false,
      equipmentInfoModal: false,
      quoteitems: [],
      columns: [
        {
          title: 'Vendor',
          align: 'left',
          width: 200,
          render: (h, params) => {
            return h('span', params.row.vendor.first_name + ' ' + params.row.vendor.last_name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.quote_status)
          }
        },
        {
          title: 'Estimated Price',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.equipment.unit_cost)
          }
        },
        {
          title: 'Quoted Price',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.quote_price)
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
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.showAccept(params.index)
                  }
                }
              }, 'Accept')
            ])
          }
        }
      ],
      quoteColumns: [
        {
          title: 'Item',
          align: 'left',
          render: (h, params) => {
            return h('span', [
              h('span', {
                on: {
                  click: () => {
                    this.showEquipmentInfo(params.index)
                  }
                }
              }, params.row.equipment.name)
            ])
          }
        },
        {
          title: 'Status',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.quote_status)
          }
        },
        {
          title: 'Quote',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.quote_price + ' ' + params.row.equipment.unit_cost_in)
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
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.showNewQuote(params.index)
                  }
                }
              }, 'Quote')
            ])
          }
        }
      ],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      quotesPageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      vendorQuotesPageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      vendorQuotes: [],
      search: {
        q: ''
      },
      currentBid: [],
      currentBidColumns: [
        {
          title: 'Vendor',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.vendor.first_name + ' ' + params.row.vendor.last_name)
          }
        },
        {
          title: 'Project',
          align: 'left',
          width: 200,
          render: (h, params) => {
            return h('span', params.row.project.name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          width: 100,
          render: (h, params) => {
            return h('span', params.row.bid_status)
          }
        }
      ],
      acceptQuoteModal: false,
      denyBidModal: false,
      selectedBid: [],
      equipments: [],
      selectedEquipment: '',
      selectedQuoteItem: [],
      formErrors: [],
      equipmentInfo: [],
      equipFormData: []
    }
  },
  methods: {
    fetchProject () {
      this.api['viewProject'](this.slug, 'get', null, null).then(res => {
        this.projectData = res.data
        if (this.projectData.bidding) {
          this.buttonText = 'Disable bidding'
        } else {
          this.buttonText = 'Enable bidding'
        }
        this.fetchEquipments()
        this.fetchQuotes()
        this.fetchQuoteItems()
        this.checkIfBidExists()
        this.fetchVendorQuoteItems()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchEquipments () {
      let params = {
        project: this.projectData.id
      }
      this.api['projectEquipments'](params).then(res => {
        this.equipments = res.data.results
      }).catch((e) => {
        let errors = e.response.data
        if (errors.non_field_errors) {
          this.$notify({
            group: 'error',
            type: 'warn',
            text: errors.non_field_errors[0]
          })
        }
      })
    },
    saveProject () {
      this.projectData.bidding = !this.projectData.bidding
      this.projectData.lead = this.projectData.lead.id
      this.api['projectView'](this.slug, 'put', null, this.projectData).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Bidding successfully updated'
        })
        this.formErrors = []
        this.fetchProject()
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
            this.projectQuotationModal = true
          }, 0)
        }
      })
    },
    paginateAction (pageNumber) {
      this.fetchQuoteItems(pageNumber)
    },
    fetchQuotes (offset) {
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q
      }
      this.api['viewQuotes']('get', params, null, null).then(res => {
        let data = res.data

        this.quotesPageData.totalRecords = data.count
        this.quotesPageData.totalPages = data.total_pages
        this.quotesPageData.currentPage = data.current_page
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchQuoteItems (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q,
        item: this.selectedEquipment
      }
      this.api['viewQuoteItems']('get', params, null, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.quoteitems = data.results
        console.log(this.quoteitems)
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
    fetchVendorQuoteItems (offset) {
      this.vendorQuotesPageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q,
        vendor: this.$store.getters.getUserId
      }
      this.api['viewQuoteItems']('get', params, null, null).then(res => {
        let data = res.data

        this.vendorQuotesPageData.totalRecords = data.count
        this.vendorQuotesPageData.totalPages = data.total_pages
        this.vendorQuotesPageData.currentPage = data.current_page

        this.vendorQuotes = data.results
        this.vendorQuotesPageData.loading = false
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
        this.vendorQuotesPageData.loading = false
      })
    },
    requestQuotation () {
      let formData = {
        project: this.projectData.id
      }
      this.api['viewQuotes']('post', null, formData).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'RFQ submitted successfully'
        })
      }).catch((e) => {
        let errors = e.response.data
        if (errors.non_field_errors) {
          this.$notify({
            group: 'error',
            type: 'warn',
            text: errors.non_field_errors[0]
          })
        }
      })
    },
    saveBid () {
      let formData = {
        project: this.projectData.id,
        vendor: this.$store.getters.getUserId,
        bid_status: 'Open'
      }
      this.api['viewBids']('post', null, formData).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Bid submitted successfully'
        })
        this.checkIfBidExists()
      }).catch((e) => {
        let errors = e.response.data
        if (errors.non_field_errors) {
          this.$notify({
            group: 'error',
            type: 'warn',
            text: errors.non_field_errors[0]
          })
        }
      })
    },
    checkIfBidExists () {
      if (this.checkPermissions.validatePermission(this.allPermissions.add_projectbid, this.$store.getters.getPermissions)) {
        let params = {
          project: this.projectData.id,
          e: true
        }
        this.api['viewBids']('get', params, null, null).then(res => {
          let data = res.data
          this.currentBid = data.results

          this.bidExists = data.count !== 0
        }).catch((e) => {
          this.$notify({
            group: 'error',
            type: 'warn',
            text: e.response.data.detail
          })
          this.pageData.loading = false
        })
      }
    },
    showAccept (index) {
      this.selectedQuoteItem = this.quoteitems[index]
      this.acceptQuoteModal = true
    },
    showDeny (index) {
      this.selectedBid = this.quoteitems[index]
      this.denyBidModal = true
    },
    showNewQuote (index) {
      this.selectedQuoteItem = this.vendorQuotes[index]
      this.newQuoteModal = true
    },
    showEquipmentInfo (index) {
      this.equipmentInfo = this.vendorQuotes[index]
      this.equipFormData = this.equipmentInfo.equipment
      this.equipmentInfoModal = true
    },
    updateQuoteStatus (slug, quoteStatus) {
      this.selectedQuoteItem.project = this.selectedQuoteItem.project.id
      this.selectedQuoteItem.quote = this.selectedQuoteItem.quote.id
      this.selectedQuoteItem.vendor = this.selectedQuoteItem.vendor.id
      this.selectedQuoteItem.equipment = this.selectedQuoteItem.equipment.id
      this.selectedQuoteItem.quote_status = quoteStatus
      console.log(this.selectedQuoteItem)

      this.api['viewQuoteItem'](this.selectedQuoteItem.slug, 'put', null, this.selectedQuoteItem).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Quote status updated successfully'
        })
        this.fetchQuoteItems()
      }).catch((e) => {
        let errors = e.response.data
        if (errors.non_field_errors) {
          this.$notify({
            group: 'error',
            type: 'warn',
            text: errors.non_field_errors[0]
          })
        }
      })
    },
    submitQuote () {
      this.selectedQuoteItem.project = this.selectedQuoteItem.project.id
      this.selectedQuoteItem.quote = this.selectedQuoteItem.quote.id
      this.selectedQuoteItem.vendor = this.selectedQuoteItem.vendor.id
      this.selectedQuoteItem.equipment = this.selectedQuoteItem.equipment.id
      this.api['viewQuoteItem'](this.selectedQuoteItem.slug, 'put', null, this.selectedQuoteItem).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Quote submitted successfully'
        })
        this.fetchVendorQuoteItems()
      }).catch((e) => {
        let errors = e.response.data
        if (errors.non_field_errors) {
          this.$notify({
            group: 'error',
            type: 'warn',
            text: errors.non_field_errors[0]
          })
        }
        this.fetchVendorQuoteItems()
      })
    }
  },
  created () {
    this.fetchProject()
  }
}
</script>

<style scoped>

</style>
