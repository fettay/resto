import React, { Component } from 'react';
import {
  ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend,
} from 'recharts';
import axios from "axios"

function format_data (x) {
  return {name: x.title , Ventes: x.count};
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

class Changelog extends Component{
  constructor(props) {
    super(props);
    console.log(props)
    this.state = {data: [
      {
        name: 'Page A', uv: 4000, Ventes: 2400, amt: 2400, pu: 9,
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
  getBars(meals_count){
    var list_resto = Object.keys(meals_count[1]);
    return list_resto.map( (x, index) => <Bar dataKey={x} barSize={40} fill={COLORS[index % 4]} />)
  }
  loadData2() {
    const token = localStorage.getItem('token');
    axios.get(process.env.REACT_APP_SERVER_URL + "/meals_count",
      {
      headers:{'Authorization': token}
      })
    .then(response => {
      var meals_count = response.data.map(format_data);
      console.log(meals_count) 
      this.setState({data: meals_count, bars: this.getBars(meals_count)})
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
      <ComposedChart
      layout="vertical"
      width={1000}
      height={9000}
      data={this.state.data}
      margin={{
        top: 20, right: 20, bottom: 20, left: 20,
      }}
    >
      <CartesianGrid stroke="#f5f5f5" />
      <XAxis type="number" />
      <YAxis dataKey="name" type="category" />
      <Tooltip />
      <Legend />
      
      {this.state.bars}
      
    </ComposedChart>
    )
  }
    
  
}

export default Changelog