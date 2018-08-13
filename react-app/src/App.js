import React, { Component } from 'react';
// import logo from './logo.svg';
import logo from './orange.svg';
import './App.css';

import { Navbar, Nav, NavItem, MenuItem, NavDropdown } from 'react-bootstrap';

class App extends Component {
  render() {
    return (
      <div className="App">
      
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">calory</h1>
        </header>
        <Navbar>
        <Navbar.Header>
        {/* <Navbar.Brand> */}
          {/* <a href="#">calory</a> */}
        {/* </Navbar.Brand> */}
        </Navbar.Header>
        <Nav>
        <NavItem eventKey={1} href="index">Home</NavItem>
        <NavItem eventKey={2} href="#">History</NavItem>
        <NavDropdown eventKey={3} title="About" id="basic-nav-dropdown">
          <MenuItem eventKey={3.1}>Action1</MenuItem>
          <MenuItem eventKey={3.2}>Action2</MenuItem>
          <MenuItem eventKey={3.3}>Action3</MenuItem>
          <MenuItem divider />
        </NavDropdown>
        </Nav>
      </Navbar>
        <p className="App-intro">
          Welcome 
          {/* To get started, edit <code>src/App.js</code> and save to reload. */}
        </p>
      </div>
    );
  }
}

export default App;
