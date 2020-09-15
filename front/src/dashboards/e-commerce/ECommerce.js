import React from 'react'
import Section8 from './Section1'
import Section1 from '../analytics/Section1'
import Section3 from './Section3'


const Dashboard = () => (
  <div>
    <div className="p-15 p-t-20 p-b-0">
      <Section8 />
    </div>
    <Section1 />
    <Section3 />
  </div>
)
export default Dashboard
