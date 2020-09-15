import React, { Component } from 'react';
import {
  BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import axios from "axios"

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

var groupBy = function(xs, key) {
    return xs.reduce(function(rv, x) {
      (rv[x[key]] = rv[x[key]] || []).push(x);
      return rv;
    }, {});
  };


function format_data (x) {
        var value = {};
        value['name'] = x[0]['day'];
        x.forEach(element => value[element['restaurant']] = element['count']);
        return(
           value 
        )
  }
  

class BarChart4 extends Component{
    constructor(props) {
      super(props);
      this.state = {data: [
        {
            name: 'Page A', uv: 4000, pv: 2400, amt: 2400, pu: 9,
          },
          {
            name: 'Page B', uv: 3000, pv: 1398, amt: 2210,pu: 9
          },
          {
            name: 'Page C', uv: 2000, pv: 9800, amt: 2290,pu: 9
          },
          {
            name: 'Page D', uv: 2780, pv: 3908, amt: 2000,pu: 9
          },
          {
            name: 'Page E', uv: 1890, pv: 4800, amt: 2181,pu: 9
          },
          {
            name: 'Page F', uv: 2390, pv: 3800, amt: 2500,pu: 900
          },
          {
            name: 'Page G', uv: 3490, pv: 4300, amt: 2100,pu: 9
          },
      ] }
    }
    getBars(rest_data){
        var list_resto = Object.keys(rest_data[1]).filter(item => item != "name");
        return list_resto.map( (x, index) => <Bar yAxisId="left" dataKey={x} fill= {COLORS[index % 4]} />)
    }
    loadData2() {
      const token = localStorage.getItem('token');
      axios.get(process.env.REACT_APP_SERVER_URL + "/orders_per_weekday?start_date=" + this.props.sliderValues[0] +'&end_date=' + this.props.sliderValues[1],
  
        {
        headers:{'Authorization': token}
        })
      .then(response => {
        var rest_data = Object.values(groupBy(response.data, "day"));
        rest_data = rest_data.map(format_data)
        console.log(rest_data) 
        this.setState({data: rest_data, bars: this.getBars(rest_data)})
      })  
    }
  
    componentDidMount(){
      var response = this.loadData2()
    }
    componentDidUpdate(prevProps){
      if(prevProps.sliderValues !== this.props.sliderValues) {
        this.loadData2()
      } 
      }
  
    
    render(){
      return(
        <BarChart
        width={500}
        height={300}
        data={this.state.data}
        margin={{
          top: 20, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
        <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
        <Tooltip />
        <Legend />
            {this.state.bars}
        </BarChart>
      )
    }
      
    
  }
  
  export default BarChart4
  