import React from 'react'
import {random} from '../../functions'
import Widget from '../../elements/DashboardWidget'
import BarChartWidget9 from '../../bar-chart-widgets/BarChartWidget9'
import BarChart from './barChartRest'



const Section3 = (props) => (
  <Widget title="Moyenne du nombre de commande reparties par jour de la semaine" description="En nombre de commande">
    <div className="row">
        <div className="col-12 col-sm-6 col-lg-6 m-b-10" >
          <BarChart sliderValues={props.sliderValues}/>
        </div>
      ))}
    </div>
  </Widget>
)
export default Section3
