import React, { Component } from 'react'
import Section1 from './Section1'
import Section2 from './Section2'
import Section3 from './Section3'
import Section4 from './Section4'
import Section5 from './Section5'
import Section6 from './Section6'
import Section7 from './Section7'
import CustomizedSlider from '../../api/slider'
import moment from 'moment'
import Badge from 'react-bootstrap/Badge'

class Dashboard extends Component {
    constructor(props) {
      super(props);
      this.sliderValues = [0, moment().format('L')];
      this.state = {sliderValues: [0, moment().format('L')]};
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
    <CustomizedSlider  
        getAriaLabel={(index) => (index === 0 ? 'Minimum price' : 'Maximum price')}
        defaultValue={[20, 40]}
        onChange={this.handleChange}
        onMouseUp={this.handleMouseUp}/>
        
    <Badge pill variant="primary" className="mr-5" className="ml-5">
    {this.state.sliderValues[0]}     
    </Badge>{' '}
  
    <Badge pill variant="primary" className="ml-5" md={{ span: 4, offset: 4 }}>
      {this.state.sliderValues[1]}     
    </Badge>{' '}
    <div className="row">
      <div className="col-12 col-md-12 col-xl-6">
        <Section2 sliderValues={this.state.sliderValues}/>
      </div>
      <div className="col-12 col-md-12 col-xl-6">
        <Section3 sliderValues={this.state.sliderValues} />
      </div>
    </div>
    <div className="row">
      <div className="col-12 col-md-12 col-xl-6">
        <Section4 sliderValues={this.state.sliderValues} />
      </div>
      
      <div className="col-12 col-md-12 col-xl-6">
        <Section5 sliderValues={this.state.sliderValues}/>
      
      </div>
      
    </div>
    <Section7 sliderValues={this.state.sliderValues} />
  </div>
      )
    }
}
export default Dashboard
