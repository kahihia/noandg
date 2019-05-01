<template>
  <div>
    <div class="top-header">
      <h1>
        <span class="text">Support</span>
      </h1>
      <div class="left-links">
          <div class="buttons">
            <div class="button-group">
            <div class="button-group">
              <button class="btn green" @click="newHelpIssue= true">New support ticket</button>
              <Modal
                v-model="newHelpIssue"
                ok-text="Submit"
                width="400"
                @on-ok="saveHelp"
                title="New support ticket">
                <p>Submit your problem to our support team.</p>
                <form>
                  <div>
                    <label for="name">Title</label>
                    <input v-model="issueForm.name" :required="issueForm.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="priority">Priority</label>
                    <Select v-model="issueForm.priority" :class="formErrors.priority === '' ? 'invalid-input':''" id="priority">
                      <Option v-for="item in priorities" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.priority">{{formErrors.priority[0]}}</span>
                  </div>
                  <div>
                    <label for="problem">What's our issue</label>
                    <textarea class="input" v-model="issueForm.problem" id="problem"></textarea>
                    <span class="input-help-error" v-if="formErrors.problem">{{formErrors.problem[0]}}</span>
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
        Manage support tickets raised.
      </span>
    </div>

    <div class="content-data">
      <Table :columns="columns" :data="helps" :loading="pageData.loading" @on-row-click="viewHelp"></Table>
      <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
    </div>
  </div>
</template>

<script>
import moment from 'moment'
export default {
  mounted () {
    if (!this.$store.getters.getLoggedIn) {
      this.$router.push({name: 'accounts_login'})
    }
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_user, this.$store.getters.getPermissions)) {
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
      newHelpIssue: false,
      priorities: [
        {
          value: 'Normal',
          label: 'Normal'
        },
        {
          value: 'Critical',
          label: 'Critical'
        },
        {
          value: 'Urgent',
          label: 'Urgent'
        }
      ],
      formErrors: [],
      issueForm: {
        name: '',
        problem: '',
        priority: ''
      },
      columns: [
        {
          title: 'Title',
          align: 'left',
          sortable: true,
          width: 250,
          render: (h, params) => {
            return h('span', params.row.name)
          }
        },
        {
          title: 'Created By',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.created_by.first_name + ' ' + params.row.created_by.last_name)
          }
        },
        {
          title: 'Status',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.status)
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
          title: 'Updates On',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', this.filterDate(params.row.updated_at))
          }
        }
      ],
      helps: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0,
        q: ''
      }
    }
  },
  methods: {
    filterDate (dateToFilter) {
      return moment(String(dateToFilter)).format('MMM Do YYYY')
    },
    viewHelp (rowData) {
      this.$router.push({name: 'help_detail', params: {slug: rowData.slug}})
    },
    fetchHelps (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        q: this.pageData.q
      }
      this.api['viewHelps']('get', params, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.helps = data.results
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
      this.fetchHelps(pageNumber)
    },
    saveHelp () {
      this.issueForm.created_by = this.$store.getters.getUserId
      this.api['viewHelps']('post', null, this.issueForm).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Support ticket successfully created'
        })
        this.formErrors = []
        this.fetchHelps()
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
            this.newHelpIssue = true
          }, 0)
        }
      })
    }
  },
  created () {
    this.fetchHelps()
  }
}
</script>

<style scoped>

</style>
