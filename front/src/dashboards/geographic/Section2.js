import React from 'react'
import Widget from '../../elements/DashboardWidget'
import VectorMap from './VectorMap'
import SamplePieChartWidget1 from '../../pie-chart-widgets/SamplePieChartWidget1'

const Section2 = (props) => (
  <div className="col-12 col-md-12 col-lg-12 m-b-12">
  <Widget
    title="Repartion du chiffre d'affaire par restaurant"
    description="En €">
    <SamplePieChartWidget1 sliderValues={props.sliderValues} />
  </Widget>
</div>
)
export default Section2
