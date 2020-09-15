export function config(
  state = {
    layout: 'default-sidebar-1',
    background: 'light',
    navbar: 'dark',
    topNavigation: 'light',
    logo: 'dark',
    leftSidebar: 'dark',
    leftSidebarIcons: 'light',
    rightSidebar: false,
    collapsed: false
  },
  action
) {
  switch (action.type) {
    case 'SET_CONFIG':
      return Object.assign({}, state, {
        ...action.config
      })
    default:
      return state
  }
}
