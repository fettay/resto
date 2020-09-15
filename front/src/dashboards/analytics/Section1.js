import React, {Component} from 'react'
import {random} from '../../functions'
import Widget from '../../elements/DashboardWidget'
import BarChartWidget9 from '../../bar-chart-widgets/BarChartWidget9'
import axios from "axios"
import Button from 'react-bootstrap/Button'

const chartData = () => {
  let data = []
  for (let i = 0; i < 20; i++) {
    data.push({name: 'Serie ' + (i + 1), value: random(20, 90)})
  }
  return data
}


const getWidgetData = (data) => {
  return ({
    color: 'info',
    height: 250,
    widget: {
      bg: 'transparent',
      color: 'info',
      title: 'Dernier mois',
      align: 'left',
      padding: 0,
      data: data
    }
  })
} 

function format_data (x) {
  return {name: x.title , value: x.count};
}


class Section1 extends Component{
  constructor(props) {
    super(props);
    this.state = {widget: getWidgetData(chartData())}
  }

  loadData2() {
    const token = localStorage.getItem('token');
    axios.get(process.env.REACT_APP_SERVER_URL + "/meals_count?top=20",
    {
    headers:{'Authorization': token}
    })
    .then(response => {
      var meals_count = response.data.map(format_data);
      console.log(meals_count) 
      this.setState({widget: getWidgetData(meals_count)})
    })  
  }

  componentDidMount(){
    var response = this.loadData2()
  }

  
  render(){
    return(
      <Widget title="Ventes par produit" description="Dernier mois(Top20)">
         <Button href="/documentation/change-log" size="sm" variant="info">voir plus</Button> {' '}
        <div className="row">
          <div className="col-12 col-sm-12 col-lg-12 m-b-12">
            <BarChartWidget9 {...this.state.widget} />
          </div>
        </div>
      </Widget>
    )
  }
    
  
}


export default Section1
