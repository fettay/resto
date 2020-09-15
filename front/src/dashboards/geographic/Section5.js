import React from 'react'
import Widget from '../../elements/DashboardWidget'
import GraphGeo from './graphGeo'

const Section5 =(props) => (
  <Widget title="Chiffre d'affaire par jour" description="Par restaurant">
    <GraphGeo sliderValues={props.sliderValues}/> 
  </Widget>
)
export default Section5
