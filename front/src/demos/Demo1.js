import {connect} from 'react-redux'
import {compose, lifecycle} from 'recompose'
import Dashboard from '../dashboards/analytics/Analytics'

const Demo1 = compose(
  connect(state => {
    return {
      config: state.config
    }
  }),
  lifecycle({
    componentDidMount() {
      this.props.dispatch({
        type: 'SET_CONFIG',
        config: {
          layout: 'default-sidebar-1',
          navbar: 'light',
          logo: 'info',
          leftSidebar: 'sucess'
        }
      })
    }
  })
)

export default (Dashboard)
