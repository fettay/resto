const urls = [
  {
    title: 'Commandes passées',
    items: [
      {
        url: '',
        icon: 'dashboard',
        title: 'Ventes',
        
        items: [
          {
            url: '/dashboards/analytics',
            icon: '',
            title: 'Ventes par restaurant',
            items: []
          },
          {
            url: '/dashboards/e-commerce',
            icon: '',
            title: 'Ventes par produit',
            items: []
          },
          {
            url: '/dashboards/e-commerce',
            icon: '',
            title: 'total',
            items: []
          }
        ]
      },
      {
        url: '',
        icon: 'bookmark_border',
        title: 'statistiques des ventes',
        items: [
          {
            url: '/demos/demo-1',
            icon: '',
            title: 'Jour',
            items: []
          },
          {
            url: '/demos/demo-2',
            icon: '',
            title: 'heure',
            items: []
          },
          
        ]
      },
      {
        url: '',
        icon: 'code',
        title: 'Produits vendus par jour',
        
        items: [
          {
            url: '/layouts/default-sidebar-1',
            icon: '',
            title: 'statistiques',
            items: []
          },
          
        ]
      },
      {
        url: '',
        icon: 'extension',
        title: 'Répartitions de ventes ',
        items: [
          {
            url: '/widgets/activity-widgets',
            icon: '',
            title: 'click and collect',
            items: []
          },
          {
            url: '/widgets/area-chart-widgets',
            icon: '',
            title: 'livraison',
            items: []
          },
          
          
          
        ]
      }
    ]
  },
  {
    title: 'Predictions',
    items: [
      {
        url: '',
        icon: 'label',
        title: 'Staffing',
        items: [
          {
            url: '/ui-elements/badges',
            icon: '',
            title: 'jour',
            items: []
          },
          {
            url: '/ui-elements/breadcrumbs',
            icon: '',
            title: 'semaine',
            items: []
          },
          {
            url: '/ui-elements/buttons',
            icon: '',
            title: 'année',
            items: []
          },
          //          {
          //            url: '/ui-elements/cards',
          //            icon: '',
          //            title: 'Cards',
          //            items: []
          //          },
          //          {
          //            url: '/ui-elements/dropdowns',
          //            icon: '',
          //            title: 'Dropdowns',
          //            items: []
          //          },
          
        ]
      },
      {
        url: '',
        icon: 'assignment',
        title: 'produits',
        
        items: [
          {
            url: '/forms/default-forms',
            icon: '',
            title: 'jour',
            items: []
          },
          {
            url: '/forms/input-groups',
            icon: '',
            title: 'semaine',
            items: []
          },
          //          {
          //            url: '/forms/steps',
          //            icon: '',
          //            title: 'Form steps',
          //            items: []
          //          },
          {
            url: '/forms/validation',
            icon: '',
            title: 'mois',
            items: []
          },
          {
            url: '/forms/sliders',
            icon: '',
            title: 'année',
            items: []
          },
           
        ]
      },
      
    ]
  },
]
export function navigation(state = Array.from(urls), action) {
  switch (action.type) {
    case 'SET_NAVIGATION':
      return Object.assign({}, state, {
        ...action.navigation
      })
    default:
      return state
  }
}
