import React,{Component} from 'react'
import {connect} from 'react-redux'
import {validate, submit} from '../../actions/pages/index'
import Form from '../Form'
import InputGroup from '../InputGroup'
import {Link, Redirect} from 'react-router-dom'
import axios from "axios"
import { MDBContainer, MDBRow, MDBCol, MDBInput, MDBBtn } from 'mdbreact';
import EmailIcon from '@material-ui/icons/Email';
import VpnKeyIcon from '@material-ui/icons/VpnKey';


/*
const Login = ({fields, submit}) => (
  <Form
    title="Login"
    description="Please enter your name and email address to login">
    {fields[0] && <InputGroup field={fields[0]} />}
    {fields[1] && <InputGroup field={fields[1]} />}
    {fields &&
      submit && (
        <div className="form-group">
          <button
            className="btn btn-primary btn-rounded btn-outline"
            type="submit"
            onClick={() => submit(fields)}>
            Submit
          </button>
        </div>
      )}
    <div className="links">
      <p>
        <span className="m-r-5">Don't have an account?</span>
        <Link to="/pages/create-account">Create account</Link>
      </p>
    </div>
  </Form>
)

const mapStateToProps = (state, ownProps) => {
  return {
    fields: state.login.fields
  }
}
const mapDispatchToProps = dispatch => {
  return {
    submit: fields => dispatch(submit(fields)),
    validate: (value, field) => dispatch(validate(value, field))
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(Login)
*/

class Login extends Component{
  constructor(props) {
    super(props);
    this.state = {
      loginError: '',
      justLoggedIn: false
      };

      this.handleSubmit = this.handleSubmit.bind(this);
      this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.name]:event.target.value
    });
  }

  handleSubmit(event) {
    const { email, password } = this.state;
    axios
      .post(
        "http://localhost:8000/login",
        {
            email: email,
            password: password,
          },
          { withCredentials: true }
      )
      .then(response => response.data)
      .then(user => {
        console.log('from login','response')
        localStorage.setItem('currentUser', JSON.stringify(user));
        localStorage.setItem('token', 'Token ' + user.token)
        this.setState({'justLoggedIn': true});

      })
      .catch(error => {
        console.log("login error", error)
      });
   event.preventDefault();   
  }

  renderForm(){
    return(
    /*
    <div>
      <form onSubmit={this.handleSubmit}>

        <input
        type="email"
        name="email"
        placeholder="email"
        value={this.state.email}
        onChange={this.handleChange}
        required
        />
        <input
        type="password"
        name="password"
        placeholder="password"
        value={this.state.password}
        onChange={this.handleChange}
        required
        />
        <div className="form-group">
        <button 
        type="submit"
        className="btn btn-primary btn-rounded btn-outline">Login</button>
        </div>
        

      </form>
    </div>)
    */
   <div className="sample-form">
   <h3>Connectez-vous</h3>
   <form onSubmit={this.handleSubmit}>
     <div className="description">Hello</div>
      <div className="input-group">
        <span className="input-group-addon rounded-left">
          <EmailIcon></EmailIcon> 
        </span>
        <input
          placeholder="Email"
          type='email'
          className='form-control rounded-right'
          name='email'
          onChange={this.handleChange}
          required
        />
        </div>
        <div className="input-group">
        <span className="input-group-addon rounded-left">
          <VpnKeyIcon> </VpnKeyIcon>
        </span>
        
        <input
          placeholder="password"
          type='password'
          className='form-control rounded-right'
          name='password'
          onChange={this.handleChange}
          required
        />
      </div>
     <div className="form-group">
          <button
            className="btn btn-primary btn-rounded btn-outline"
            type="submit">
            Submit
          </button>
      </div>
   </form>
 </div>
    )}
  render(){
    if((JSON.parse(localStorage.getItem('currentUser')) != null)){
      return <Redirect to="./demos/demo-1"/>
    }
    else if(this.state.justLoggedIn){
      return <Redirect to="./demos/demo-1"/>
    }
    return this.renderForm()    
  }
}

export default Login;
