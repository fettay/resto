import React from 'react'
import PropTypes from 'prop-types'
import '../css/activity-widgets/activity-widget-1.css'
import axios from "axios"
import moment from 'moment'
import Moment from 'react-moment';
import 'moment/min/moment-with-locales'


moment.locale('fr');

const ActivityWidget11 = ({items, amount}) => (
  <div className="activity-widget-1">
    <table className="table table-striped table-unbordered">
      <tbody>
      
        {items.slice(0, amount).map((item, i) => (
          <tr key={i}>
            <td>
              <span>
                {item.type}
              </span>
            </td>
            <td>{item.title}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)

ActivityWidget11.defaultProps = {
  amount: 10
}

ActivityWidget11.propTypes = {
  items: PropTypes.arrayOf(PropTypes.object).isRequired,
  amount: PropTypes.number
}

export default ActivityWidget11