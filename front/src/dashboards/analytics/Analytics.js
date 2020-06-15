import React from 'react'
import Section1 from './Section1'
import Section2 from './Section2'
import Section3 from './Section3'
import Section4 from './Section4'
import Section5 from './Section5'
import Section6 from './Section6'
import Section7 from './Section7'

const Dashboard = () => (
  <div>
    <Section1 />
    <div className="row">
      <div className="col-12 col-md-12 col-xl-6">
        <Section2 />
      </div>
      <div className="col-12 col-md-12 col-xl-6">
        <Section3 />
      </div>
    </div>
   
  </div>
)
export default Dashboard
