import React, { Component } from 'react'
import Widget from '../../elements/DashboardWidget'
import Number from '../../user-widgets/UserWidget2'
import users from '../../json/users.json'
import axios from 'axios'
import Card from 'react-bootstrap/Card'
import CardDeck from 'react-bootstrap/CardDeck'
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';
import { number } from 'prop-types'
import { BsBag, BsStar } from 'react-icons/bs';
import { AiOutlineDollar } from 'react-icons/ai';

function color () { 
  if (5>0) {
    return (
      "text-success"
    )
    
  } else {
    return(
      "text-danger"
    )
  }
  
}
console.log(color)

class Section4 extends Component {
  constructor(props) {
    super(props);
    this.state = { data: {
                          orders: {value: '...', change: '...'},
                          sales: {value: '...', change: '...'},
                          sales_avg: {value: '...', change: '...'},
                          reviews: {value: '...', change: '...'}

                        }
                  }
                 
  }
  loadData(){
    const token = localStorage.getItem('token');
    axios.get(process.env.REACT_APP_SERVER_URL + "/top_numbers?",
      {
        headers:{'Authorization': token}
      })
      .then(response => {
        var created = response.data;
         
        this.setState({data:created})
        console.log(created.orders.value);
      })
      
      .catch(error => {
        console.log(error);
      })
  }
  componentDidMount(){
    var response = this.loadData()
  }
  componentDidUpdate(prevProps){
    if(prevProps.sliderValues !== this.props.sliderValues) {
      this.loadData()
    } 
    }
  render() {
  
     
     
    return(
      <Widget title="Chiffres important sur une semaine" description="">
      <CardDeck>
      <Card className="bg-warning" > 
        <Card.Body className="text-center">
        <h3>  <BsBag /> </h3>
          <Card.Title className="text-white"> {this.state.data.orders.value} (commandes)</Card.Title>
          <Card.Text></Card.Text>
          <Card.Subtitle  className="text-danger">  {Math.round(this.state.data.orders.change)}%</Card.Subtitle>
          <Card.Text>
           
          </Card.Text>
        </Card.Body>
        <Card.Footer className="text-center">
          <small className="text-white">Nombre de commande</small>
        </Card.Footer>
      </Card>
      <Card className="bg-warning">
        <Card.Body className="text-center">
        <h3>  <AiOutlineDollar /> </h3>
          <Card.Title className="text-white">{Math.round(this.state.data.sales.value)}€</Card.Title>
          <Card.Text>    </Card.Text>
          <Card.Subtitle className="text-danger">{Math.round(this.state.data.sales.change)}%</Card.Subtitle>
          <Card.Text>
         
          </Card.Text>
        </Card.Body>
        <Card.Footer className="text-center">
          <small className="text-white">Ventes</small>
        </Card.Footer>
      </Card>
      <Card className="bg-warning">
        <Card.Body className="text-center">
        <h3>  <BsBag /> </h3>
          <Card.Title className="text-white">{Math.round(this.state.data.sales_avg.value)}€</Card.Title>
          <Card.Text></Card.Text>
          <Card.Subtitle className="text-success">{Math.round(this.state.data.sales_avg.change)}%</Card.Subtitle>
          <Card.Text>
        
          </Card.Text>
        </Card.Body>
        <Card.Footer className="text-center">
          <small className="text-white">Panier moyen</small>
        </Card.Footer>
      </Card>
      <Card className="bg-warning">
        <Card.Body className="text-center">
        <h3>  <BsStar /> </h3>
          <Card.Title className="text-white">{Math.round(this.state.data.reviews.value)}</Card.Title>
          <Card.Text></Card.Text>
          <Card.Subtitle className="text-success">{Math.round(this.state.data.reviews.change)}%</Card.Subtitle>
          <Card.Text>
          
          </Card.Text>
        </Card.Body>
        <Card.Footer className="text-center">
          <small className="text-white">Reviews</small>
        </Card.Footer>
      </Card>
    </CardDeck>
    </Widget>

   
    )

  }
  
 
}
export default Section4
