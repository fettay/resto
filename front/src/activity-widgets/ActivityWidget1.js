import React from 'react'
import PropTypes from 'prop-types'
import '../css/activity-widgets/activity-widget-1.css'
import axios from "axios"
import moment from 'moment'
import Moment from 'react-moment'
import 'moment/min/moment-with-locales'


moment.locale('fr');

const ActivityWidget1 = ({items, amount}) => (
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
            <td>
          <Moment fromNow className="text-xs">{item.date}</Moment>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)

ActivityWidget1.defaultProps = {
  amount: 10
}

ActivityWidget1.propTypes = {
  items: PropTypes.arrayOf(PropTypes.object).isRequired,
  amount: PropTypes.number
}

export default ActivityWidget1
/*

class ActivityWidget1 extends Component{
  constructor(props) {
    super(props);
    this.state = {data}
  } 
  loadData2(){
    const token = localStorage.getItem('token');
    axios
    .get(
      "http://localhost:8000/orders_counts",
      {
        headers:{'Authorization': token}
      })
      .then()
    }



}
*/