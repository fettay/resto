import React from 'react'
import Widget from '../../elements/DashboardWidget'
import AreaChart from './AreaChart'

const Section2 = (props) => (
  <Widget title="Nombre de ventes" description="Par jour">
    <div className="row">
      <div className="col">
        <AreaChart sliderValues={props.sliderValues}/>
      </div>
    </div>
  </Widget>
)
export default Section2
