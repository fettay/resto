import React, {Component} from 'react'
import Widget from '../../elements/DashboardWidget'
import ActivityWidget1 from '../../activity-widgets/ActivityWidget1'
import sales from '../../json/sales-2.json'
import Last from './last'
import { thresholdFreedmanDiaconis } from 'd3'
import axios from "axios"


/*
const Section3 = () => (
  <Widget title="Sales stream" description="Latest sales and customer actions">
    <ActivityWidget1 items={sales} amount={6} />
  </Widget>
)
*/

function format_data2 (x) {
  return { 'date': x.date ,'title': x.restaurant, 'type': x.amount + '€' };
}

class Section3 extends Component{
  constructor(props) {
    super(props);
    this.state = {data: []}
  }

loadData2() {
  const token = localStorage.getItem('token');
  axios
  .get(
  "http://localhost:8000/last_orders",

    {
    headers:{'Authorization': token}
    })
  .then(response => {
    var last_orders = response.data.map(format_data2);
    console.log(last_orders) 
    this.setState({data: last_orders})
  })  
}

componentDidMount(){
  var response = this.loadData2()
}

  
  render(){
    return(
      <Widget title="Sales stream" description="Latest sales and customer actions">
        <ActivityWidget1 items={this.state.data} amount={6} />
      </Widget>
    )
  }
    
  
}




export default Section3
