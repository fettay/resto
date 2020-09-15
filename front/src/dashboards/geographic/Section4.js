import React from 'react'
import Widget from '../../elements/DashboardWidget'
import TimelineWidget1 from '../../timeline-widgets/TimelineWidget1'
import timeline from '../../json/timeline.json'


const Section4 = (props) => (
  <Widget title="Nombre de commande par jour" description="Par restaurant">
    <TimelineWidget1 items={timeline} sliderValues={props.sliderValues}/>
  </Widget>

)
export default Section4
