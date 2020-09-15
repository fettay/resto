import React from 'react'
import Widget from '../../elements/DashboardWidget'
import TableWidget4 from '../../table-widgets/TableWidget4'
import orders from '../../json/orders.json'

const Section7 = (props) => (
  <div className="row shipping-status">
    <div className="col">
      <Widget title="Shipping status" description="Latest online sales">
        <TableWidget4 sliderValues={props.sliderValues} />
      </Widget>
    </div>
  </div>
)
export default Section7
