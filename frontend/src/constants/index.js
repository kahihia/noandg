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
const RM_GROUP_USER = DOMAIN + 'users/remove/user/'

// Eng
const PROJECTS_DIRECTORY = DOMAIN + 'engineering/projects/'
const PROJECT_STAGE = DOMAIN + 'engineering/projectstage/'
const CREATE_PROJECT = DOMAIN + 'engineering/create/project/'
const PROJECTS_FORM = DOMAIN + 'engineering/forms/projects/'
const PROJECT_LEADS = DOMAIN + 'engineering/forms/leads/'
const PROJECT_TEAMS = DOMAIN + 'engineering/forms/teams/'
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
const FABRICATIONS_DIRECTORY = DOMAIN + 'engineering/fabrications/'
const CREATE_FABRICATION = DOMAIN + 'engineering/create/fabrication/'

// Log
const LG_CREATE_PROJECT = DOMAIN + 'logistics/create/project/'
const LG_BID_DIRECTORY = DOMAIN + 'logistics/bids/'
const LG_CREATE_BID = DOMAIN + 'logistics/create/bid/'
const LG_QUOTE_DIRECTORY = DOMAIN + 'logistics/quotes/'
const LG_CREATE_QUOTE = DOMAIN + 'logistics/create/quote/'
const LG_PROJECT_EQUIPMENTS = DOMAIN + 'logistics/forms/equipments/'
const LG_QUOTE_ITEM_DIRECTORY = DOMAIN + 'logistics/quoteitems/'
const LG_CREATE_QUOTE_ITEM = DOMAIN + 'logistics/create/quoteitem/'

// Compliance
const SURVEYS_DIRECTORY = DOMAIN + 'compliance/surveys/'
const CREATE_SURVEY = DOMAIN + 'compliance/create/survey/'
const QUESTIONS_DIRECTORY = DOMAIN + 'compliance/questions/'
const ANSWERS_DIRECTORY = DOMAIN + 'compliance/answers/'
const CREATE_ANSWER = DOMAIN + 'compliance/create/answer/'

// Warehouse
const WAREHOUSE_DIRECTORY = DOMAIN + 'warehouse/list/'
const STOCK_DIRECTORY = DOMAIN + 'warehouse/stocks/'
const CREATE_STOCK = DOMAIN + 'warehouse/create/stock/'
const STOCK_RELEASE_DIRECTORY = DOMAIN + 'warehouse/stock/releases/'
const CREATE_STOCK_RELEASE = DOMAIN + 'warehouse/create/stocks/release/'
const STOCK_FORM = DOMAIN + 'warehouse/form/stock/'

// Construction
const CIVIL_DIRECTORY = DOMAIN + 'construction/civil/'
const CREATE_CIVIL = DOMAIN + 'construction/create/civil/'

// Help
const HELP_DIRECTORY = DOMAIN + 'compliance/help/'
const CREATE_HELP = DOMAIN + 'compliance/create/help/'

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
  RM_GROUP_USER,
  CREATE_USER_GROUPS_URL,
  USER_PERMISSIONS_URL,
  USER_PLANS_URL,
  USER_PROFILE_URL,
  USERS_FORM_URL,
  PROJECTS_DIRECTORY,
  PROJECT_STAGE,
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
  PROJECTS_FORM,
  QUOTE_ITEM_DIRECTORY,
  CREATE_QUOTE_ITEM,
  DESIGNS_DIRECTORY,
  CREATE_DESIGN,
  FABRICATIONS_DIRECTORY,
  CREATE_FABRICATION,
  PROJECT_TEAMS,
  LG_CREATE_PROJECT,
  LG_BID_DIRECTORY,
  LG_CREATE_BID,
  LG_QUOTE_DIRECTORY,
  LG_CREATE_QUOTE,
  LG_PROJECT_EQUIPMENTS,
  LG_QUOTE_ITEM_DIRECTORY,
  LG_CREATE_QUOTE_ITEM,
  SURVEYS_DIRECTORY,
  CREATE_SURVEY,
  QUESTIONS_DIRECTORY,
  ANSWERS_DIRECTORY,
  CREATE_ANSWER,
  WAREHOUSE_DIRECTORY,
  STOCK_DIRECTORY,
  CREATE_STOCK,
  STOCK_RELEASE_DIRECTORY,
  CREATE_STOCK_RELEASE,
  STOCK_FORM,
  CIVIL_DIRECTORY,
  CREATE_CIVIL,
  HELP_DIRECTORY,
  CREATE_HELP
}
