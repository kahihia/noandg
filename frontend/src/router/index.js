import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import NotFound from '../components/common/NotFound'

import Login from '../components/accounts/Login'
import Logout from '../components/accounts/Logout'

import ParentUsers from '../components/users/ParentUsers'
import Users from '../components/users/users/Users'
import Groups from '../components/users/groups/Groups'
import ViewGroup from '../components/users/groups/ViewGroup'

import ParentEngineering from '../components/engineering/ParentEngineering'
import Projects from '../components/engineering/projects/Projects'
import ParentProject from '../components/engineering/project/ProjectParent'
import ProjectTeam from '../components/engineering/project/Team'
import ProjectStage from '../components/engineering/project/ProjectStage'
import ProjectFiles from '../components/engineering/project/Files'
import ProjectBudget from '../components/engineering/project/Budget'
import ProjectBidding from '../components/engineering/project/Bidding'
import ProjectQuotation from '../components/engineering/project/Quotation'
import ProjectDesigns from '../components/engineering/project/Designs'
import ProjectFabrication from '../components/engineering/project/Fabrication'
import AnswerFabrication from '../components/engineering/project/AnswerFabrication'

import ParentLogistics from '../components/logistics/ParentLogistics'
import LogisticsProjects from '../components/logistics/projects/Projects'
import LogisticsParentProject from '../components/logistics/project/ProjectParent'
import LogisticsProjectBidding from '../components/logistics/project/Bidding'
import LogisticsProjectQuotation from '../components/logistics/project/Quotation'

import ParentCompliance from '../components/compliance/ParentCompliance'
import Surveys from '../components/compliance/surveys/Surveys'
import Survey from '../components/compliance/surveys/Survey'

import ParentWarehouse from '../components/warehouses/ParentWarehouse'
import Warehouses from '../components/warehouses/wh/Warehouses'
import Warehouse from '../components/warehouses/wh/Warehouse'

import ParentConstruction from '../components/construction/ParentConstruction'
import CivilProjects from '../components/construction/civil/Projects'
import ProjectParentConstruction from '../components/construction/civil/ProjectParent'
import Civil from '../components/construction/civil/Civil'
import CivilAnswers from '../components/construction/civil/AnswerCivil'
import Commission from '../components/construction/civil/Commission'

import ParentReports from '../components/reports/ParentReports'
import ReportSummary from '../components/reports/Summary'
import ReportProject from '../components/reports/ProjectReport'

import Help from '../components/compliance/help/Help'
import HelpDetail from '../components/compliance/help/HelpDetail'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '*',
      name: 'not_found',
      component: NotFound,
      meta: {
        title: '404 Error',
        requiresAuth: false
      }
    },
    {
      path: '/',
      name: 'reg_home',
      component: HelloWorld,
      meta: {
        title: 'Home',
        requiresAuth: true
      }
    },
    {
      path: '/home',
      name: 'home',
      component: HelloWorld,
      meta: {
        title: 'Home',
        requiresAuth: true
      },
      redirect: '/engineering/projects'
    },
    {
      path: '/login',
      name: 'accounts_login',
      component: Login,
      meta: {
        title: 'Log in',
        requiresAuth: false
      }
    },
    {
      path: '/logout',
      name: 'accounts_logout',
      component: Logout,
      meta: {
        title: 'Log out',
        requiresAuth: false
      }
    },
    {
      path: '/users',
      name: 'users',
      component: ParentUsers,
      meta: {
        title: 'Users',
        requiresAuth: true
      },
      redirect: '/users/directory',
      children: [
        {
          path: 'directory',
          name: 'users_directory',
          component: Users,
          meta: {
            title: 'Users',
            requiresAuth: true
          }
        },
        {
          path: 'groups',
          name: 'groups_directory',
          component: Groups,
          meta: {
            title: 'Groups',
            requiresAuth: true
          }
        },
        {
          path: 'groups/:slug',
          name: 'group_view',
          component: ViewGroup,
          meta: {
            title: 'Group Details',
            requiresAuth: true
          }
        }
      ]
    },
    {
      path: '/engineering',
      name: 'engineering',
      component: ParentEngineering,
      meta: {
        title: 'Engineering',
        requiresAuth: true
      },
      children: [
        {
          path: 'projects',
          name: 'projects_directory',
          component: Projects,
          meta: {
            title: 'Projects',
            requiresAuth: true
          }
        },
        {
          path: 'projects/:slug',
          name: 'project_details',
          component: ParentProject,
          meta: {
            title: 'Project',
            requiresAuth: true
          },
          redirect: '/engineering/projects/:slug/overview',
          children: [
            {
              path: 'team',
              name: 'project_team',
              component: ProjectTeam,
              meta: {
                title: 'Project Team',
                requiresAuth: true
              }
            },
            {
              path: 'overview',
              name: 'project_overview',
              component: ProjectStage,
              meta: {
                title: 'Project Overview',
                requiresAuth: true
              }
            },
            {
              path: 'files',
              name: 'project_files',
              component: ProjectFiles,
              meta: {
                title: 'Project Files',
                requiresAuth: true
              }
            },
            {
              path: 'budget',
              name: 'project_budget',
              component: ProjectBudget,
              meta: {
                title: 'Project Budget',
                requiresAuth: true
              }
            },
            {
              path: 'bidding',
              name: 'project_bidding',
              component: ProjectBidding,
              meta: {
                title: 'Project Bidding',
                requiresAuth: true
              }
            },
            {
              path: 'quotation',
              name: 'project_quotation',
              component: ProjectQuotation,
              meta: {
                title: 'Project Quotation',
                requiresAuth: true
              }
            },
            {
              path: 'fabrication',
              name: 'project_fabrication',
              component: ProjectFabrication,
              meta: {
                title: 'Project',
                requiresAuth: true
              }
            },
            {
              path: 'fabrication/answer/:fabrication_slug',
              name: 'answer_fabrication',
              component: AnswerFabrication,
              meta: {
                title: 'Answer Fabrication',
                requiresAuth: true
              }
            },
            {
              path: 'designs',
              name: 'project_designs',
              component: ProjectDesigns,
              meta: {
                title: 'Project Designs',
                requiresAuth: true
              }
            }
          ]
        }
      ]
    },
    {
      path: '/logistics',
      name: 'logistics',
      component: ParentLogistics,
      meta: {
        title: 'Logistics',
        requiresAuth: true
      },
      children: [
        {
          path: 'projects',
          name: 'logistics_directory',
          component: LogisticsProjects,
          meta: {
            title: 'Projects',
            requiresAuth: true
          }
        },
        {
          path: 'projects/:slug',
          name: 'logistics_project_details',
          component: LogisticsParentProject,
          meta: {
            title: 'Project',
            requiresAuth: true
          },
          redirect: '/logistics/projects/:slug/bidding',
          children: [
            {
              path: 'bidding',
              name: 'logistics_project_bidding',
              component: LogisticsProjectBidding,
              meta: {
                title: 'Project Bidding',
                requiresAuth: true
              }
            },
            {
              path: 'quotation',
              name: 'logistics_project_quotation',
              component: LogisticsProjectQuotation,
              meta: {
                title: 'Project Quotation',
                requiresAuth: true
              }
            }
          ]
        }
      ]
    },
    {
      path: '/compliance',
      name: 'compliance',
      component: ParentCompliance,
      meta: {
        title: 'Compliance',
        requiresAuth: true
      },
      children: [
        {
          path: 'surveys',
          name: 'surveys_directory',
          component: Surveys,
          meta: {
            title: 'Surveys',
            requiresAuth: true
          }
        },
        {
          path: 'surveys/:slug',
          name: 'survey_details',
          component: Survey,
          meta: {
            title: 'Survey',
            requiresAuth: true
          }
        }
      ]
    },
    {
      path: '/warehouse',
      name: 'warehouse',
      component: ParentWarehouse,
      meta: {
        title: 'warehouse',
        requiresAuth: true
      },
      children: [
        {
          path: 'warehouses',
          name: 'warehouses_directory',
          component: Warehouses,
          meta: {
            title: 'warehouses',
            requiresAuth: true
          }
        },
        {
          path: 'warehouses/:slug',
          name: 'warehouse_details',
          component: Warehouse,
          meta: {
            title: 'warehouse',
            requiresAuth: true
          }
        }
      ]
    },
    {
      path: '/construction',
      name: 'construction',
      component: ParentConstruction,
      meta: {
        title: 'construction',
        requiresAuth: true
      },
      redirect: '/construction/projects',
      children: [
        {
          path: 'projects',
          name: 'civil_projects_directory',
          component: CivilProjects,
          meta: {
            title: 'civil projects',
            requiresAuth: true
          }
        },
        {
          path: 'project',
          name: 'construction_project',
          component: ProjectParentConstruction,
          meta: {
            title: 'cons',
            requiresAuth: true
          },
          redirect: '/construction/project/civil/:slug',
          children: [
            {
              path: 'civil/:slug',
              name: 'civil',
              component: Civil,
              meta: {
                title: 'civil',
                requiresAuth: true
              }
            },
            {
              path: 'civil/:slug/survey/:survey_slug',
              name: 'civil_survey',
              component: CivilAnswers,
              meta: {
                title: 'Civil Survey',
                requiresAuth: true
              }
            },
            {
              path: 'commissioning/:slug',
              name: 'commissioning',
              component: Commission,
              meta: {
                title: 'commissioning',
                requiresAuth: true
              }
            }
          ]
        }
      ]
    },
    {
      path: '/reports',
      name: 'reports',
      component: ParentReports,
      meta: {
        title: 'Reports',
        requiresAuth: true
      },
      redirect: '/reports/summary',
      children: [
        {
          path: 'summary',
          name: 'report_summary',
          component: ReportSummary,
          meta: {
            title: 'Summary reports',
            requiresAuth: true
          }
        },
        {
          path: 'project/:slug',
          name: 'report_project',
          component: ReportProject,
          meta: {
            title: 'Project reports',
            requiresAuth: true
          }
        }
      ]
    },
    {
      path: '/help',
      name: 'help',
      component: Help,
      meta: {
        title: 'Help',
        requiresAuth: true
      }
    },
    {
      path: '/help/:slug',
      name: 'help_detail',
      component: HelpDetail,
      meta: {
        title: 'Help',
        requiresAuth: true
      }
    }
  ]
})
