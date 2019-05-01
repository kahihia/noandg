<template>
  <div>
    <div class="top-header">
      <h1>
        <span class="text">Support</span>
      </h1>
    </div>

    <div class="bottom-header">
      <h1>
        <span class="text">Manage support ticket</span>
      </h1>
      <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button class="btn gray" @click="assignHelpIssue= true">Assign User</button>
              <Modal
                v-model="assignHelpIssue"
                ok-text="Submit"
                width="400"
                @on-ok="solveHelp"
                title="Solve ticket">
                <p>Assign a given user to manage this issue.</p>
                <form>
                  <div>
                    <label for="eassigned_to">Assign To</label>
                    <Select v-model="helpForm.assigned_to" id="eassigned_to">
                      <Option v-for="item in users" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.assigned_to">{{formErrors.assigned_to[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
            <div class="button-group">
              <button class="btn green" @click="solveHelpIssue= true">Solve ticket</button>
              <Modal
                v-model="solveHelpIssue"
                ok-text="Submit"
                width="400"
                @on-ok="solveHelp"
                title="Solve ticket">
                <p>Submit your solution offered or recommendation.</p>
                <form>
                  <div>
                    <label for="solution">Solution/Recommendation</label>
                    <textarea class="input" v-model="helpForm.solution" id="solution"></textarea>
                    <span class="input-help-error" v-if="formErrors.solution">{{formErrors.solution[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
          </div>
        </div>
    </div>

    <div class="page-info">
      <span>
        Manage support tickets raised.
      </span>
    </div>

    <div class="m-l-20">
      <Row class="m-b-20" :gutter="8">
        <i-col span="16">
          <div class="content-data">
            <div class="content-data-header">
              <span>Ticket details</span>
            </div>
            <div class="box-shadow-top">
              <div class="ticket-card">
                <div class="ticket-card-header">User Details</div>
                <div class="ticket-card-body">Issue raised by {{help.created_by.first_name}} {{help.created_by.last_name}}</div>
              </div>
              <div class="ticket-card">
                <div class="ticket-card-header">Problem experienced</div>
                <div class="ticket-card-body">{{help.problem}}</div>
              </div>
              <div class="ticket-card">
                <div class="ticket-card-header">Solution</div>
                <div class="ticket-card-body">
                  <p v-if="help.solution">{{help.solution}}</p>
                  <p v-else>Ticket not resolved</p>
                </div>
              </div>
            </div>
          </div>
        </i-col>
        <i-col span="8">
          <div class="content-data">
            <div class="ticket-card">
              <div class="ticket-card-header">Assigned to</div>
              <div class="ticket-card-body">
                <p v-if="help.assigned_to">{{help.assigned_to.first_name}} {{help.assigned_to.last_name}}</p>
                <p v-else>No user assigned</p>
              </div>
            </div>
          </div>
          <div class="content-data">
            <div class="ticket-card">
              <div class="ticket-card-header">Ticket status</div>
              <div class="ticket-card-body">
                <p>{{help.status}}</p>
              </div>
            </div>
          </div>
        </i-col>
      </Row>
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
      solveHelpIssue: false,
      assignHelpIssue: false,
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
      helpForm: [],
      users: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0,
        q: ''
      },
      help: [],
      slug: this.$route.params.slug
    }
  },
  methods: {
    filterDate (dateToFilter) {
      return moment(String(dateToFilter)).format('MMM Do YYYY')
    },
    fetchUsers () {
      this.api['usersForm']().then(res => {
        this.users = res.data.results
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchHelp () {
      this.api['viewHelp'](this.slug, 'get', null, null).then(res => {
        this.help = res.data
        this.fetchHelpForm()
        this.fetchUsers()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchHelpForm () {
      this.api['viewHelpForm'](this.slug, 'get').then(res => {
        this.helpForm = res.data
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
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
    },
    solveHelp () {
      this.helpForm.status = 'Solved'
      this.api['viewHelp'](this.slug, 'put', null, this.helpForm).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Support ticket successfully created'
        })
        this.formErrors = []
        this.fetchHelp()
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
            this.solveHelpIssue = true
          }, 0)
        }
      })
    },
    assignHelp () {
      this.api['viewHelp'](this.slug, 'put', null, this.helpForm).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Support ticket successfully assigned to user'
        })
        this.formErrors = []
        this.fetchHelp()
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
            this.assignHelpIssue = true
          }, 0)
        }
      })
    }
  },
  created () {
    this.fetchHelp()
  }
}
</script>

<style scoped>

</style>
