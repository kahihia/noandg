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
import ProjectOverview from '../components/engineering/project/Overview'
import ProjectFiles from '../components/engineering/project/Files'
import ProjectBudget from '../components/engineering/project/Budget'
import ProjectBidding from '../components/engineering/project/Bidding'
import ProjectQuotation from '../components/engineering/project/Quotation'

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
      }
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
              path: 'overview',
              name: 'project_overview',
              component: ProjectOverview,
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
              component: ParentProject,
              meta: {
                title: 'Project',
                requiresAuth: true
              }
            }
          ]
        }
      ]
    }
  ]
})
