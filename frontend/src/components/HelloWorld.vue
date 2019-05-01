<template>
  <div>
    <div class="top-header">
        <h1>
          <span class="text">Dashboard</span>
        </h1>
    </div>
    <div style="padding-left: 15px">
      <Row>
        <i-col span="8">
          <Card>
            <p slot="title">Total Projects</p>
            <div v-if="projectsCount === 0" class="homeCard-body null">
              <i class="icon-null-state"></i>
              <div>No projects yet</div>
            </div>
            <div v-else class="dashChart">
              <div class="textChartPane">
                <div class="textChart">
                  <div class="textChart-text">{{projectsCount}}</div>
                </div>
              </div>
            </div>
          </Card>
        </i-col>
      </Row>
    </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      projectsCount: '',
      usersCount: ''
    }
  },
  methods: {
    fetchProjects () {
      this.api['projectsDirectory']('get', null, null).then(res => {
        let data = res.data
        this.projectsCount = data.count
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    fetchUsers () {
      this.api['usersDirectory']('get', null, null).then(res => {
        let data = res.data
        this.usersCount = data.count
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    }
  },
  mounted () {
    this.fetchProjects()
    this.fetchUsers()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home .ivu-row {
  margin-right: -9px !important;
  margin-left: -9px !important;
}
.home .ivu-col-span-8 {
  padding-right: 9px !important;
  padding-left: 9px !important;
}
.home .ivu-card-bordered {
  border: none !important;
  border-bottom: 2px solid #d6d9dc !important;
  margin-bottom: 18px !important;
  border-radius: 0 !important;
  height: 300px !important;
}
.home .ivu-card-head {
  height: 50px !important;
  margin-left: 10px !important;
  margin-right: 10px !important;
}
.ivu-card-head p, .ivu-card-head-inner {
  font-size: 18px !important;
  font-weight: 500 !important;
  color: #2996cc !important;
}
.ivu-card-head {
  border-bottom: 1px solid #d6d9dc !important;
  padding: 14px 6px !important;
}
.ivu-card-body {
  display: table !important;
  height: calc(100% - 50px) !important;
  width: 100% !important;
  padding: 0 16px !important;
}
.homeCard-body {
  display: table-cell;
  vertical-align: middle;
  text-align: center;
  font-weight: 300;
  opacity: 1;
  visibility: visible;
  -webkit-transition: all .25s;
  transition: all .25s;
}
.homeCard-body.null {
  font-size: 22px;
  line-height: 1.715;
}
</style>
