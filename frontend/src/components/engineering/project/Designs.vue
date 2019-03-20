<template>
    <div>
      <div class="bottom-header">
        <h1>
          <span class="text">Designs & Procedures</span>
        </h1>

        <div class="left-links">
          <div class="buttons">
            <div class="button-group">
              <button v-if="this.checkPermissions.validatePermission(this.allPermissions.add_projectfile, this.$store.getters.getPermissions)" class="btn green" @click="newDesignModal= true">Upload design</button>
              <Modal
                v-model="newDesignModal"
                ok-text="Upload design"
                @on-ok="uploadDesign"
                width="400"
                title="Upload a new design">
                <p>You can upload any designs or procedures required in this project on this page.</p>
                <form method="post" enctype="multipart/form-data">
                  <div>
                    <label for="name">Designs's name</label>
                    <input v-model="formData.name" :required="formData.name"
                         :class="formErrors.name ? 'invalid-input':''"
                           class="input" type="text" value="" name="name" placeholder="" id="name">
                    <span class="input-help-error" v-if="formErrors.name">{{formErrors.name[0]}}</span>
                  </div>
                  <div>
                    <label for="design_type">Type</label>
                    <Select v-model="formData.design_type" id="design_type">
                      <Option v-for="item in designTypes" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                    <span class="input-help-error" v-if="formErrors.design_type">{{formErrors.design_type[0]}}</span>
                  </div>
                  <div>
                    <label for="description">Description</label>
                    <textarea v-model="formData.description" :required="formData.description"
                         :class="formErrors.description ? 'invalid-input':''"
                              class="input" name="description" placeholder="" id="description"></textarea>
                    <span class="input-help-error" v-if="formErrors.description">{{formErrors.description[0]}}</span>
                  </div>
                  <div>
                    <label for="document">Select file</label>
                    <input @change="onFileChange" :required="formData.document"
                         :class="formErrors.document ? 'invalid-input':''"
                           class="input" ref="file" type="file" name="document" placeholder="" id="document">
                    <span class="input-help-error" v-if="formErrors.document">{{formErrors.document[0]}}</span>
                  </div>
                </form>
              </Modal>
            </div>
          </div>
        </div>
      </div>

       <div class="page-info">
        <span>
          Designs and procedures includes all documents ranging from <strong>FEED</strong> (Front End Engineering Design), <strong>HAZOP</strong> (Hazard and Operability Study), and Modeling.
        </span>
      </div>

      <div class="content-data">
        <Modal
          v-model="viewFileModal"
          ok-text="Delete file"
          width="600"
          title="File preview">
          <p>You can preview and delete a given file.</p>
          <br/>
          <iframe width="565" height="400" :src="'https://docs.google.com/gview?url='+selectedFile.document+'&embedded=true'"></iframe>
        </Modal>
        <Table :columns="columns" :data="files" :loading="pageData.loading"></Table>
        <Page v-if="!pageData.loading && pageData.totalPages > 1" :total="pageData.totalRecords" :current="pageData.currentPage" @on-change="paginateAction" />
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      newDesignModal: false,
      viewFileModal: false,
      selectedFile: [],
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
          title: 'Type',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('span', params.row.design_type)
          }
        },
        {
          title: 'Preview',
          align: 'left',
          sortable: true,
          render: (h, params) => {
            return h('Button', {
              props: {
                type: 'default',
                size: 'small'
              },
              style: {
                marginRight: '5px'
              },
              on: {
                click: () => {
                  this.showPreviewFile(params.index)
                }
              }
            }, 'View')
          }
        }
      ],
      projectData: [],
      slug: this.$route.params.slug,
      files: [],
      pageData: {
        loading: false,
        totalRecords: 0,
        totalPages: 0,
        currentPage: 0
      },
      search: {
        q: ''
      },
      formErrors: [],
      formData: {
        name: '',
        description: '',
        project: '',
        design_type: '',
        document: ''
      },
      designTypes: [
        {
          value: 'FEED',
          label: 'FEED'
        },
        {
          value: 'HAZOP',
          label: 'HAZOP'
        },
        {
          value: 'MODELING',
          label: 'MODELING'
        }
      ]
    }
  },
  methods: {
    showPreviewFile (index) {
      this.selectedFile = this.files[index]
      this.viewFileModal = true
    },
    onFileChange (e) {
      this.formData.document = this.$refs.file.files[0]
    },
    fetchProject () {
      this.api['viewProject'](this.slug, 'get', null, null).then(res => {
        this.projectData = res.data

        this.fetchDesigns()
      }).catch((e) => {
        this.$notify({
          group: 'error',
          type: 'warn',
          text: e.response.data.detail
        })
      })
    },
    paginateAction (pageNumber) {
      this.fetchDesigns(pageNumber)
    },
    fetchDesigns (offset) {
      this.pageData.loading = true
      let params = {
        limit: this.constants.PAGE_LIMIT,
        offset: offset,
        project: this.projectData.id,
        q: this.search.q
      }
      this.api['viewDesigns']('get', params, null, null).then(res => {
        let data = res.data

        this.pageData.totalRecords = data.count
        this.pageData.totalPages = data.total_pages
        this.pageData.currentPage = data.current_page

        this.files = data.results
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
    uploadDesign () {
      let postData = new FormData()
      postData.append('name', this.formData.name)
      postData.append('design_type', this.formData.design_type)
      postData.append('description', this.formData.description)
      postData.append('project', this.projectData.id)
      postData.append('document', this.formData.document)
      this.api['viewDesigns']('post', null, postData, true).then(res => {
        // success
        this.$notify({
          group: 'success',
          type: 'success',
          text: 'Design successfully uploaded'
        })
        this.formErrors = []
        this.fetchDesigns()
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
            this.newDesignModal = true
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
    if (!this.checkPermissions.validatePermission(this.allPermissions.view_projectfile, this.$store.getters.getPermissions)) {
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
