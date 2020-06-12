import React, { Component } from 'react'
import {connect} from 'react-redux'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  Tooltip
} from 'recharts'
import axios from 'axios'

function format_data (x) {
  return {'name': x.created_day, 'Nb ventes': x.count };
}


class SampleAreaChart extends Component{
  constructor(props) {
    super(props);
    this.state = {data: [
                  {name: 'Monday', USA: 4000, UK: 2400, MX: 2400},
                  {name: 'Tuesday', USA: 3000, UK: 1398, MX: 2210},
                  {name: 'Wednesday', USA: 2000, UK: 9800, MX: 2290},
                  {name: 'Thursday', USA: 2780, UK: 3908, MX: 2000},
                  {name: 'Friday', USA: 1890, UK: 4800, MX: 2181},
                  {name: 'Saturday', USA: 2390, UK: 3800, MX: 2500},
                  {name: 'Sunday', USA: 3490, UK: 4300, MX: 2100}
                  ]}
  }
  loadData(){
    const token = localStorage.getItem('token');
    axios
    .get(
      "http://localhost:8000/orders_counts",
      {
        headers:{'Authorization': token}
      })
      .then(response => {
        var created = response.data.map(format_data);
        console.log(created) 
        this.setState({data: created})
      })
      .catch(error => {
        console.log(error);
      })
  }
  componentDidMount(){
    var response = this.loadData()
  }
  transformData(response){
    var created = response.data.map(x => x.created_day);
    console.log(created) 
  }

  render(){
    return(
      <ResponsiveContainer width="100%" height={287}>
        <AreaChart data={this.state.data} margin={{top: 0, right: 0, left: 0, bottom: 0}}>
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip labelFormatter={e => this.state.data[e].name} />
          <Area
            type="monotone"
            dataKey="Nb ventes"
            stackId="1"
            stroke="#d32f2f"
            fill="#d32f2f"
          />
          <Area
            type="monotone"
            dataKey="UK"
            stackId="1"
            stroke="#ffa000"
            fill="#ffa000"
          />
          <Area
            type="monotone"
            dataKey="MX"
            stackId="1"
            stroke="#303f9f"
            fill="#303f9f"
          />
        </AreaChart>
      </ResponsiveContainer>
    )
  }
}

export default SampleAreaChart
