import React from 'react'
import {Link} from 'react-router-dom'
import '../../css/elements/logo.css'

const Logo = () => (
  <Link
    to="/demos/demo-1"
    className="logo d-flex justify-content-start align-items-center flex-nowrap">
    <i className="fa fa-code" />
    <span className="title" >ForeCast Eat</span>
  </Link>
)

export default Logo
