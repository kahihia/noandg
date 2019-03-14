import axios from 'axios'
import constants from '../constants/index'
import Vue from 'vue'

export default {

  // Login
  login (method, data) {
    return ajax(constants.LOGIN_URL, method, {data})
  },
  // users
  usersDirectory (method, params, data) {
    if (params !== null) {
      return ajax(constants.USER_LIST_URL, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_USER_URL, method, {data})
    } else {
      return ajax(constants.USER_LIST_URL, method)
    }
  },
  userGroups (method, params, data) {
    if (params !== null) {
      return ajax(constants.USER_GROUPS_URL, method, {params})
    }
  },
  userGroupsForm () {
    return ajax(constants.FORM_USER_GROUPS_URL, 'get')
  },
  createGroup (method, params, data) {
    if (data !== null) {
      return ajax(constants.CREATE_USER_GROUPS_URL, method, {data})
    }
  },
  viewGroup (slug, method, params, data) {
    if (data !== null) {
      return ajax(constants.CREATE_USER_GROUPS_URL + slug + '/', method, {data})
    } else {
      return ajax(constants.CREATE_USER_GROUPS_URL + slug + '/', method)
    }
  },
  groupPermissions (method) {
    return ajax(constants.USER_PERMISSIONS_URL, method)
  },
  // Projects
  projectsDirectory (method, params, data) {
    if (params !== null) {
      return ajax(constants.PROJECTS_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_PROJECT, method, {data})
    } else {
      return ajax(constants.PROJECTS_DIRECTORY, method)
    }
  },
  projectView (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.PROJECTS_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_PROJECT + slug + '/', method, {data})
    } else {
      return ajax(constants.PROJECTS_DIRECTORY + slug + '/', method)
    }
  },
  projectLeads () {
    return ajax(constants.PROJECT_LEADS, 'get')
  },
  viewProject (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.PROJECTS_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_PROJECT, method, {data})
    } else {
      return ajax(constants.PROJECTS_DIRECTORY + slug + '/', method)
    }
  },
  viewFiles (method, params, data, headers) {
    if (params !== null) {
      return ajax(constants.FILES_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_FILE, method, {data}, headers)
    } else {
      return ajax(constants.FILES_DIRECTORY, method)
    }
  },
  viewEquipments (method, params, data) {
    if (params !== null) {
      return ajax(constants.EQUIPMENT_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_EQUIPMENT, method, {data})
    } else {
      return ajax(constants.EQUIPMENT_DIRECTORY, method)
    }
  },
  viewEquipment (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.EQUIPMENT_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_EQUIPMENT + slug + '/', method, {data})
    } else {
      return ajax(constants.CREATE_EQUIPMENT + slug + '/', method)
    }
  },
  viewBudgets (method, params, data) {
    if (params !== null) {
      return ajax(constants.BUDGET_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_BUDGET, method, {data})
    } else {
      return ajax(constants.BUDGET_DIRECTORY, method)
    }
  },
  viewBudget (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.BUDGET_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_BUDGET + slug + '/', method, {data})
    } else {
      return ajax(constants.CREATE_BUDGET + slug + '/', method)
    }
  },
  viewBids (method, params, data) {
    if (params !== null) {
      return ajax(constants.BID_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_BID, method, {data})
    } else {
      return ajax(constants.BID_DIRECTORY, method)
    }
  },
  viewBid (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.BID_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_BID + slug + '/', method, {data})
    } else {
      return ajax(constants.BID_DIRECTORY + slug + '/', method)
    }
  },
  viewBidExists (method, params, data) {
    if (params !== null) {
      return ajax(constants.BID_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_BID, method, {data})
    } else {
      return ajax(constants.BID_DIRECTORY, method)
    }
  },
  viewQuotes (method, params, data) {
    if (params !== null) {
      return ajax(constants.QUOTE_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_QUOTE, method, {data})
    } else {
      return ajax(constants.QUOTE_DIRECTORY, method)
    }
  },
  projectEquipments (params) {
    return ajax(constants.PROJECT_EQUIPMENTS, 'get', {params})
  },
  viewQuoteItems (method, params, data) {
    if (params !== null) {
      return ajax(constants.QUOTE_ITEM_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_QUOTE_ITEM, method, {data})
    } else {
      return ajax(constants.QUOTE_ITEM_DIRECTORY, method)
    }
  },
  viewQuoteItem (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.QUOTE_ITEM_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_QUOTE_ITEM + slug + '/', method, {data})
    } else {
      return ajax(constants.QUOTE_ITEM_DIRECTORY + slug + '/', method)
    }
  }
}

/**
 * @param url
 * @param method get|post|put|delete...
 * @param params like queryString. if a url is index?a=1&b=2, params = {a: '1', b: '2'}
 * @param data post data, use for method put|post
 * @param headers post form data
 * @returns {Promise}
 */
function ajax (url, method, options, headers = null) {
  if (options !== undefined) {
    var {params = {}, data = {}} = options
  } else {
    params = data = {}
  }
  if (headers === true) {
    let config = {
      headers: {
        'Authorization': axios.defaults.headers.Authorization,
        'Content-Type': 'multipart/form-data'
      }
    }
    Vue.prototype.$http = axios
    axios.defaults.headers = config.headers
  }
  return new Promise((resolve, reject) => {
    axios({
      url,
      method,
      params,
      data
    }).then(res => {
      resolve(res)
    }, res => {
      reject(res)
      // Vue.prototype.$error(res.data.data)
    })
  })
}
