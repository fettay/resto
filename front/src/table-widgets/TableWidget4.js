import '../css/timeline-widgets/timeline-widget-1.css'
import React, { Component } from 'react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  Tooltip
} from 'recharts'
import axios from 'axios'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

var groupBy = function(xs, key) {
  return xs.reduce(function(rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
};

function format_data (x) {
  var value = {};
  value['date'] = x[0]['created_day'];
  x.forEach(element => value[element['restaurant__name']] = Math.round(element['count']));
  return(
     value 
  )
}
class TableWidejet4 extends Component{
  constructor(props) {
    super(props);
    this.state = {data: [
                  {name: 'Monday', USA: 4000, UK: 2400, MX: 2400, TS: 2466} ,
                  {name: 'Tuesday', USA: 3000, UK: 1398, MX: 2210},
                  {name: 'Wednesday', USA: 2000, UK: 9800, MX: 2290},
                  {name: 'Thursday', USA: 2780, UK: 3908, MX: 2000},
                  {name: 'Friday', USA: 1890, UK: 4800, MX: 2181},
                  {name: 'Saturday', USA: 2390, UK: 3800, MX: 2500},
                  {name: 'Sunday', USA: 3490, UK: 4300, MX: 2100}
                  ]}
  }
  getBars(rest_data){
    var list_resto = Object.keys(rest_data[1]);
    return list_resto.map( (x, index) => <Area
    type="monotone"
    dataKey={x}
    stackId="1"
    stroke={COLORS[index % 4]}
    fill={COLORS[index % 4]}
  />)
}
  loadData(){
    const token = localStorage.getItem('token');
    axios.get(process.env.REACT_APP_SERVER_URL + "/sales_resto_average?start_date=" + this.props.sliderValues[0] +'&end_date=' + this.props.sliderValues[1],
      {
        headers:{'Authorization': token}
      })
      .then(response => {
        var rest_data = Object.values(groupBy(response.data, "created_day"));
        console.log(rest_data) 
        rest_data = rest_data.map(format_data)
         
        this.setState({data: rest_data, bars: this.getBars(rest_data)})
        console.log(this.state.data)
      })
      .catch(error => {
        console.log(error);
      })
  }
  componentDidMount(){
    var response = this.loadData()
  }
  componentDidUpdate(prevProps){
    if(prevProps.sliderValues !== this.props.sliderValues) {
      this.loadData()
    } 
  }

  render(){
    return(
      <ResponsiveContainer width="100%" height={287}>
        <AreaChart data={this.state.data} margin={{top: 0, right: 0, left: 0, bottom: 0}}>
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip labelFormatter={e => this.state.data[e].name}x />
          {this.state.bars}
        </AreaChart>
      </ResponsiveContainer>
    )
  }
}

export default TableWidejet4
