const DOMAIN = '/api/v1/'

// Users
const LOGIN_URL = DOMAIN + 'accounts/login/'

// Users
const USER_LIST_URL = DOMAIN + 'users/list/'
const FORM_USER_GROUPS_URL = DOMAIN + 'users/forms/groups/'
const CREATE_USER_URL = DOMAIN + 'users/create/employee/'
const USER_GROUPS_URL = DOMAIN + 'users/groups/'
const CREATE_USER_GROUPS_URL = DOMAIN + 'users/create/group/'
const USER_PERMISSIONS_URL = DOMAIN + 'users/permissions/'
const USER_PLANS_URL = DOMAIN + 'users/plans/'
const USER_PROFILE_URL = DOMAIN + 'users/profiles/'
const USERS_FORM_URL = DOMAIN + 'users/forms/users/'

// Eng
const PROJECTS_DIRECTORY = DOMAIN + 'engineering/projects/'
const CREATE_PROJECT = DOMAIN + 'engineering/create/project/'
const PROJECT_LEADS = DOMAIN + 'engineering/forms/leads/'
const FILES_DIRECTORY = DOMAIN + 'engineering/files/'
const CREATE_FILE = DOMAIN + 'engineering/create/file/'
const DESIGNS_DIRECTORY = DOMAIN + 'engineering/designs/'
const CREATE_DESIGN = DOMAIN + 'engineering/create/design/'
const EQUIPMENT_DIRECTORY = DOMAIN + 'engineering/equipments/'
const CREATE_EQUIPMENT = DOMAIN + 'engineering/create/equipment/'
const BUDGET_DIRECTORY = DOMAIN + 'engineering/budgets/'
const CREATE_BUDGET = DOMAIN + 'engineering/create/budget/'
const BID_DIRECTORY = DOMAIN + 'engineering/bids/'
const CREATE_BID = DOMAIN + 'engineering/create/bid/'
const QUOTE_DIRECTORY = DOMAIN + 'engineering/quotes/'
const CREATE_QUOTE = DOMAIN + 'engineering/create/quote/'
const PROJECT_EQUIPMENTS = DOMAIN + 'engineering/forms/equipments/'
const QUOTE_ITEM_DIRECTORY = DOMAIN + 'engineering/quoteitems/'
const CREATE_QUOTE_ITEM = DOMAIN + 'engineering/create/quoteitem/'

export default {
  LIMIT: 10000,
  PAGE_LIMIT: 10,
  DEFAULT_PAGE_1: 1,
  NOTIF_TIMEOUT: 5000,
  NOTIF_NEVER_TIMEOUT: -1,
  ONE_DAY: 1,
  SEVEN_DAYS: 7,
  THIRTY_DAYS: 30,
  LOGIN_URL,
  USER_LIST_URL,
  FORM_USER_GROUPS_URL,
  CREATE_USER_URL,
  USER_GROUPS_URL,
  CREATE_USER_GROUPS_URL,
  USER_PERMISSIONS_URL,
  USER_PLANS_URL,
  USER_PROFILE_URL,
  USERS_FORM_URL,
  PROJECTS_DIRECTORY,
  CREATE_PROJECT,
  PROJECT_LEADS,
  FILES_DIRECTORY,
  CREATE_FILE,
  EQUIPMENT_DIRECTORY,
  CREATE_EQUIPMENT,
  BUDGET_DIRECTORY,
  CREATE_BUDGET,
  BID_DIRECTORY,
  CREATE_BID,
  QUOTE_DIRECTORY,
  CREATE_QUOTE,
  PROJECT_EQUIPMENTS,
  QUOTE_ITEM_DIRECTORY,
  CREATE_QUOTE_ITEM,
  DESIGNS_DIRECTORY,
  CREATE_DESIGN
}
