import React, {Component} from 'react'
import {ResponsiveContainer, PieChart, Pie, Cell, Tooltip} from 'recharts'
import axios from "axios"



const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

function format_data (x) {
  return {name: x.restaurant__name , value: Math.round(x.count)};
}

class PieChart3 extends Component{
  constructor(props) {
    super(props);
    console.log(props)
    this.state = {data: [
                          { name: 'Group A', value: Math.round(400) }, 
                          { name: 'Group C', value: 300 }, 
                          { name: 'Group E', value: 278 }, 
                          { name: 'Group F', value: 189 },
    ] }
  }

  loadData2() {
    const token = localStorage.getItem('token');
    axios.get(process.env.REACT_APP_SERVER_URL + "/sales_total?start_date=" + this.props.sliderValues[0] +'&end_date=' + this.props.sliderValues[1],
      {
      headers:{'Authorization': token}
      })
    .then(response => {
      var meals_count = response.data.map(format_data);
      console.log(meals_count) 
      this.setState({data: meals_count})
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
      <div>
      <ResponsiveContainer width={'100%'} height={200}>
      <PieChart>
        <Tooltip />
        <Pie data={this.state.data} dataKey="value" fill="#8884d8">
        {this.state.data.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
        </Pie>
      </PieChart>
      </ResponsiveContainer>
</div>
    )
  }
    
  
}

export default PieChart3
