import React, { Component} from 'react'
import PropTypes from 'prop-types'
import '../css/user-widgets/user-widget-2.css'
import { render } from 'react-dom';
import axios from 'axios'
import Card from 'react-bootstrap/Card'
import CardDeck from 'react-bootstrap/CardDeck'

/* const UserWidget2 = ({users, amount}) => (
  <div className="user-widget-2">
    <ul className="list-unstyled">
      {users.slice(0, amount).map((user, i) => (
        <li className="media" key={i}>
          <img
            className="rounded-circle d-flex align-self-center"
            src={user.img}
            alt=""
          />
          <div className="media-body">
            <h5>{user.name}</h5>
            <p>{user.company}</p>
            <p>
              <span className="badge badge-outline badge-sm badge-info badge-pill">
                sed
              </span>
              <span className="badge badge-outline badge-sm badge-primary badge-pill">
                sed
              </span>
              <span className="badge badge-outline badge-sm badge-danger badge-pill">
                voluptatem
              </span>
            </p>
          </div>
          <i
            className={`d-flex align-self-center fa fa-dot-circle-o color-${user.color}`}
          />
        </li>
      ))}
    </ul>
  </div>
)

UserWidget2.defaultProps = {
  amount: 10
}

UserWidget2.propTypes = {
  users: PropTypes.arrayOf(PropTypes.object),
  amount: PropTypes.number
}

export default UserWidget2

*/

const Number = ({items}) => (


      <CardDeck>
  <Card>
    <Card.Img variant="top" src="holder.js/100px160" />
    <Card.Body>
      <Card.Title> {items} </Card.Title>
      <Card.Text>
        This is a wider card with supporting text below as a natural lead-in to
        additional content. This content is a little bit longer.
      </Card.Text>
    </Card.Body>
    <Card.Footer>
      <small className="text-muted">Last updated 3 mins ago</small>
    </Card.Footer>
  </Card>
  <Card>
    <Card.Img variant="top" src="holder.js/100px160" />
    <Card.Body>
      <Card.Title>Card title</Card.Title>
      <Card.Text>
        This card has supporting text below as a natural lead-in to additional
        content.{' '}
      </Card.Text>
    </Card.Body>
    <Card.Footer>
      <small className="text-muted">Last updated 3 mins ago</small>
    </Card.Footer>
  </Card>
  <Card>
    <Card.Img variant="top" src="holder.js/100px160" />
    <Card.Body>
      <Card.Title>Card title</Card.Title>
      <Card.Text>
        This is a wider card with supporting text below as a natural lead-in to
        additional content. This card has even longer content than the first to
        show that equal height action.
      </Card.Text>
    </Card.Body>
    <Card.Footer>
      <small className="text-muted">Last updated 3 mins ago</small>
    </Card.Footer>
  </Card>
</CardDeck>
    )

  



export default Number