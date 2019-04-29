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
  viewUser (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.USER_LIST_URL + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_USER_URL + slug + '/', method, {data})
    } else {
      return ajax(constants.USER_LIST_URL + slug + '/', method)
    }
  },
  rmUser (method, params) {
    return ajax(constants.RM_GROUP_USER, method, {params})
  },
  userGroups (method, params, data) {
    if (params !== null) {
      return ajax(constants.USER_GROUPS_URL, method, {params})
    }
  },
  userGroupsForm () {
    return ajax(constants.FORM_USER_GROUPS_URL, 'get')
  },
  usersForm () {
    return ajax(constants.USERS_FORM_URL, 'get')
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
  projectEdit (slug, method, params, data) {
    return ajax(constants.CREATE_PROJECT + slug + '/', method)
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
  viewProjectStages (method, params, data) {
    if (params !== null) {
      return ajax(constants.PROJECT_STAGE, method, {params})
    } else if (data !== null) {
      return ajax(constants.PROJECT_STAGE, method, {data})
    } else {
      return ajax(constants.PROJECT_STAGE, method)
    }
  },
  viewProjectStage (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.PROJECT_STAGE + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.PROJECT_STAGE + slug + '/', method, {data})
    } else {
      return ajax(constants.PROJECT_STAGE + slug + '/', method)
    }
  },
  projectTeams (params) {
    return ajax(constants.PROJECT_TEAMS, 'get', {params})
  },
  viewProject (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.PROJECTS_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_PROJECT + slug + '/', method, {data})
    } else {
      return ajax(constants.PROJECTS_DIRECTORY + slug + '/', method)
    }
  },
  viewCrudProject (slug, method, params, data) {
    return ajax(constants.LG_CREATE_PROJECT, method, {data})
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
  viewDesigns (method, params, data, headers) {
    if (params !== null) {
      return ajax(constants.DESIGNS_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_DESIGN, method, {data}, headers)
    } else {
      return ajax(constants.DESIGNS_DIRECTORY, method)
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
  },
  viewFabrications (method, params, data) {
    if (params !== null) {
      return ajax(constants.FABRICATIONS_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_FABRICATION, method, {data})
    } else {
      return ajax(constants.FABRICATIONS_DIRECTORY, method)
    }
  },
  viewFabrication (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.FABRICATIONS_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_FABRICATION + slug + '/', method, {data})
    } else {
      return ajax(constants.FABRICATIONS_DIRECTORY + slug + '/', method)
    }
  },
  viewFabricationDelete (slug, method) {
    return ajax(constants.CREATE_FABRICATION + slug + '/', method)
  },
  viewLgBids (method, params, data) {
    if (params !== null) {
      return ajax(constants.LG_BID_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.LG_CREATE_BID, method, {data})
    } else {
      return ajax(constants.LG_BID_DIRECTORY, method)
    }
  },
  viewLgBid (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.LG_BID_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.LG_CREATE_BID + slug + '/', method, {data})
    } else {
      return ajax(constants.LG_BID_DIRECTORY + slug + '/', method)
    }
  },
  viewLgBidExists (method, params, data) {
    if (params !== null) {
      return ajax(constants.LG_BID_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.LG_CREATE_BID, method, {data})
    } else {
      return ajax(constants.LG_BID_DIRECTORY, method)
    }
  },
  viewLgQuotes (method, params, data) {
    if (params !== null) {
      return ajax(constants.LG_QUOTE_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.LG_CREATE_QUOTE, method, {data})
    } else {
      return ajax(constants.LG_QUOTE_DIRECTORY, method)
    }
  },
  projectLgEquipments (params) {
    return ajax(constants.LG_PROJECT_EQUIPMENTS, 'get', {params})
  },
  projectForm (params) {
    return ajax(constants.PROJECTS_FORM, 'get', {params})
  },
  stockForm (params) {
    return ajax(constants.STOCK_FORM, 'get', {params})
  },
  viewLgQuoteItems (method, params, data) {
    if (params !== null) {
      return ajax(constants.LG_QUOTE_ITEM_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.LG_CREATE_QUOTE_ITEM, method, {data})
    } else {
      return ajax(constants.LG_QUOTE_ITEM_DIRECTORY, method)
    }
  },
  viewLgQuoteItem (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.LG_QUOTE_ITEM_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.LG_CREATE_QUOTE_ITEM + slug + '/', method, {data})
    } else {
      return ajax(constants.LG_QUOTE_ITEM_DIRECTORY + slug + '/', method)
    }
  },
  viewSurveys (method, params, data) {
    if (params !== null) {
      return ajax(constants.SURVEYS_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_SURVEY, method, {data})
    } else {
      return ajax(constants.SURVEYS_DIRECTORY, method)
    }
  },
  viewSurveyItem (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.SURVEYS_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_SURVEY + slug + '/', method, {data})
    } else {
      return ajax(constants.SURVEYS_DIRECTORY + slug + '/', method)
    }
  },
  viewSurveyQuestions (method, params, data) {
    if (params !== null) {
      return ajax(constants.QUESTIONS_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.QUESTIONS_DIRECTORY, method, {data})
    } else {
      return ajax(constants.QUESTIONS_DIRECTORY, method)
    }
  },
  viewSurveyQuestionAnswers (method, params, data) {
    if (params !== null) {
      return ajax(constants.ANSWERS_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_ANSWER, method, {data})
    } else {
      return ajax(constants.ANSWERS_DIRECTORY, method)
    }
  },
  viewSurveyQuestionAnswer (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.ANSWERS_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_ANSWER + slug + '/', method, {data})
    } else {
      return ajax(constants.ANSWERS_DIRECTORY + slug + '/', method)
    }
  },
  viewWarehouses (method, params, data) {
    if (params !== null) {
      return ajax(constants.WAREHOUSE_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.WAREHOUSE_DIRECTORY, method, {data})
    } else {
      return ajax(constants.WAREHOUSE_DIRECTORY, method)
    }
  },
  viewWarehouse (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.WAREHOUSE_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.WAREHOUSE_DIRECTORY + slug + '/', method, {data})
    } else {
      return ajax(constants.WAREHOUSE_DIRECTORY + slug + '/', method)
    }
  },
  viewStocks (method, params, data) {
    if (params !== null) {
      return ajax(constants.STOCK_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_STOCK, method, {data})
    } else {
      return ajax(constants.STOCK_DIRECTORY, method)
    }
  },
  viewStock (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.STOCK_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_STOCK + slug + '/', method, {data})
    } else {
      return ajax(constants.STOCK_DIRECTORY + slug + '/', method)
    }
  },
  viewReleaseStocks (method, params, data) {
    if (params !== null) {
      return ajax(constants.STOCK_RELEASE_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_STOCK_RELEASE, method, {data})
    } else {
      return ajax(constants.STOCK_RELEASE_DIRECTORY, method)
    }
  },
  viewCivils (method, params, data) {
    if (params !== null) {
      return ajax(constants.CIVIL_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_CIVIL, method, {data})
    } else {
      return ajax(constants.CIVIL_DIRECTORY, method)
    }
  },
  viewCivil (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.CIVIL_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_CIVIL + slug + '/', method, {data})
    } else {
      return ajax(constants.CIVIL_DIRECTORY + slug + '/', method)
    }
  },
  viewHelps (method, params, data) {
    if (params !== null) {
      return ajax(constants.HELP_DIRECTORY, method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_HELP, method, {data})
    } else {
      return ajax(constants.HELP_DIRECTORY, method)
    }
  },
  viewHelp (slug, method, params, data) {
    if (params !== null) {
      return ajax(constants.HELP_DIRECTORY + slug + '/', method, {params})
    } else if (data !== null) {
      return ajax(constants.CREATE_HELP + slug + '/', method, {data})
    } else {
      return ajax(constants.HELP_DIRECTORY + slug + '/', method)
    }
  },
  viewHelpForm (slug, method) {
    return ajax(constants.CREATE_HELP + slug + '/', method)
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
  } else {
    let config = {
      headers: {
        'Authorization': axios.defaults.headers.Authorization,
        'Content-Type': 'application/json'
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
