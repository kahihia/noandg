<template>
    <div>
      <div class="page-header page-header-inner">
        <div class="page-header-left">
          <h1>
            <div class="text">Bidding</div>
          </h1>
        </div>
         <div class="page-header-right">
            <div class="buttons">
              <div v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)" class="button-group">
                <button :class="projectData.bidding ? 'btn-delete':'btn-blue'" @click="projectBiddingModal= true">{{buttonText}}</button>
                <Modal
                  :class="projectData.bidding ? 'delete-group':''"
                  v-model="projectBiddingModal"
                  :ok-text="buttonText"
                  @on-ok="saveProject"
                  width="400"
                  title="Change project bidding status">
                  <p>When you enable bidding, all registered vendors will be able to place bids which you can assess and accept or deny the user from submitting a quote.</p>
                </Modal>
              </div>
              <div class="button-group">
                <button class="btn-gray" @click.prevent="fetchProject">Refresh</button>
              </div>
            </div>
         </div>
      </div>

      <div class="page-info">
        <span v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)">
          Manage project bidding and the list of vendors who can submit quotes on this project.
        </span>
        <span v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectbid, this.$store.getters.getPermissions) && this.projectData.bidding">
          This project is open for bidding and vendors are able to submit their bids.
        </span>
        <span v-else>
          This project is currently not open for bidding.
        </span>
      </div>

      <div class="content-data">
        <div class="content-row" v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectbid, this.$store.getters.getPermissions)">
          <div class="content-are-one">
            <div v-if="!bidExists && this.projectData.bidding">
              <legend>Submit your bid</legend>
              <p>You can submit your bid by clicking on the <strong>Submit bid</strong> button bellow. You'll be requested to submit a quotation if your bid is accepted.</p>
              <br/>
              <button class="btn-blue" @click="newBidModal= true">Submit bid</button>
              <Modal
                v-model="newBidModal"
                ok-text="Submit bid"
                @on-ok="saveBid"
                width="400"
                title="Submit your project bid">
                <p>You are about to submit your bid on this project.</p>
            </Modal>
            </div>
            <div v-if="bidExists">
              <legend>Check bid status</legend>
              <Alert v-if="bidExists && currentBid[0].bid_status === 'Open'" show-icon>
                You have already submitted your bid on this project. You can check the status of your bid below.
              </Alert>
              <Alert type="success" v-if="bidExists && currentBid[0].bid_status === 'Accepted'" show-icon>
                Your bid was accepted. Check on <strong>quotation</strong> page to submit your quote.
              </Alert>
              <Alert type="warning" v-if="bidExists && currentBid[0].bid_status === 'Denied'" show-icon>
                Your bid was denied. Your cannot bid again or submit any quotes on this project.
              </Alert>
              <Table :columns="currentBidColumns" :data="currentBid"></Table>
            </div>
          </div>
          <div v-if="bidExists || !bidExists && this.projectData.bidding" class="content-area-two">
            <div class="content-info">
              <div class="content-info-card">
                <h4>What you need to know</h4>
                <ul>
                  <li>You can only bid once on this project</li>
                  <li>Bidding won't be enabled even if your current bid was denied.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div v-if="this.checkPermissions.validatePermission(this.allPermissions.change_project, this.$store.getters.getPermissions)">
          <Table :columns="columns" :data="bids" :loading="pageData.loading"></Table>
          <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
          <!-- modals -->
          <Modal
            v-model="acceptBidModal"
            ok-text="Accept bid"
            @on-ok="updateBidStatus(selectedBid.slug, 'Accepted')"
            width="400"
            title="Accept vendor bid">
            <p>When you accept this bid, this vendor will be able to send a quote once a request for quotation is made.</p>
          </Modal>
          <Modal
            class="delete-group"
            v-model="denyBidModal"
            ok-text="Deny bid"
            @on-ok="updateBidStatus(selectedBid.slug, 'Denied')"
            width="400"
            title="Deny vendor bid">
            <p>When you deny this bid, this vendor will not be able to bid on this project again or send a quote once a request for quotation is made.</p>
          </Modal>
        </div>
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
      projectBiddingModal: false,
      newBidModal: false,
      bids: [],
      columns: [
        {
          title: 'Vendor',
          align: 'left',
          render: (h, params) => {
            return h('span', params.row.vendor.first_name + ' ' + params.row.vendor.last_name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          width: 200,
          render: (h, params) => {
            return h('span', params.row.bid_status)
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
              }, 'Accept'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.showDeny(params.index)
                  }
                }
              }, 'Deny')
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
      acceptBidModal: false,
      denyBidModal: false,
      selectedBid: []
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
        this.fetchBids()
        this.checkIfBidExists()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
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
            this.projectBiddingModal = true
          }, 0)
        }
      })
    },
    paginateAction (pageNumber) {
      this.fetchBids(pageNumber)
    },
    fetchBids (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q
      }
      this.api['viewBids']('get', params, null, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.bids = data.results
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
    saveBid () {
      let formData = {
        project: this.projectData.id,
        vendor: this.$store.getters.getUserId,
        bid_status: 'Open',
        rfq: false
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
      this.selectedBid = this.bids[index]
      this.acceptBidModal = true
    },
    showDeny (index) {
      this.selectedBid = this.bids[index]
      this.denyBidModal = true
    },
    updateBidStatus (slug, bidStatus) {
      let formData = {
        bid_status: bidStatus,
        project: this.selectedBid.project.id,
        vendor: this.selectedBid.vendor.id,
        rfq: this.selectedBid.rfq
      }
      this.api['viewBid'](slug, 'put', null, formData).then(res => {
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Bid status updated successfully'
        })
        this.fetchBids()
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
    }
  },
  created () {
    this.fetchProject()
  }
}
</script>

<style scoped>

</style>
