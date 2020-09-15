import React, {Component} from 'react'
import Section1 from './Section1'
import Section2 from './Section2'
import Section3 from './Section3'
import Section4 from './Section4'
import Section5 from './Section5'
import Section6 from './Section6'
import Section7 from './Section7'
import Chart from './last'
import CustomizedSlider from '../../api/slider'
import moment from 'moment'

class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.sliderValues = [0, 100];
    this.state = {sliderValues: [0, 100]};
    this.start =moment('2020-06-01') ;
  }
  
   handleChange = (event, newValue) => {
    this.sliderValues = [this.start.clone().add(newValue[0], "day").format('YYYY-MM-DD') , this.start.clone().add(newValue[1], "day").format('YYYY-MM-DD')];
    console.log(this.sliderValues)
  };
  handleMouseUp = (event) => {
    this.setState({sliderValues: this.sliderValues});
  }

  render() {
    return(
      <div>
        
    <div className="col-12 col-md-12 col-xl-12">
        <Section4 sliderValues={this.state.sliderValues}/>
      </div>
    <div className="row">
      <div className="col-12 col-md-12 col-xl-6">
        <Section2 sliderValues={this.state.sliderValues}/>
      </div>
      <div className="col-12 col-md-12 col-xl-6">
        <Section3 sliderValues={this.state.sliderValues}/>
      </div>
      <div className="row" className="col-12 col-md-12 col-xl-12">
        <Section1 sliderValues={this.state.sliderValues}/>
      </div>
    </div>
   
  </div>
    )
  }

}
export default Dashboard
