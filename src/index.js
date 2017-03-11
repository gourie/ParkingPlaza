/*
*   Author: Joeri Nicolaes
*   ======================
*/

import React from 'react'
import { render } from 'react-dom'
import { browserHistory, Router, Route, Link, withRouter } from 'react-router'

const App = withRouter(
  React.createClass({

    getInitialState() {
      return {
        tacos: [
          { name: 'duck confit' },
          { name: 'carne asada' },
          { name: 'shrimp' }
        ]
      }
    },

    addTaco() {
      let name = prompt('taco name?')

      this.setState({
        tacos: this.state.tacos.concat({ name })
      })
    },

    handleRemoveTaco(removedTaco) {
      this.setState({
        tacos: this.state.tacos.filter(function (taco) {
          return taco.name != removedTaco
        })
      })

      this.props.router.push('/')
    },

    render() {
      let links = this.state.tacos.map(function (taco, i) {
        return (
          <li key={i}>
            <Link to={`/taco/${taco.name}`}>{taco.name}</Link>
          </li>
        )
      })
      return (
        <div className="App">
          <button onClick={this.addTaco}>Add Taco</button>
          <ul className="Master">
            {links}
          </ul>
          <div className="Detail">
            {this.props.children && React.cloneElement(this.props.children, {
              onRemoveTaco: this.handleRemoveTaco
            })}
          </div>
        </div>
      )
    }
  })
)

const Taco = React.createClass({
  remove() {
    this.props.onRemoveTaco(this.props.params.name)
  },

  render() {
    return (
      <div className="Taco">
        <h1>{this.props.params.name}</h1>
        <button onClick={this.remove}>remove</button>
      </div>
    )
  }
})

render((
  <Router history={browserHistory}>
    <Route path="/test" component={App}>
      <Route path="taco/:name" component={Taco} />
    </Route>
  </Router>
), document.getElementById('testDiv'))

//import App from './Test/App';
//import ParkingList from './Components/ParkingList';
//import React from 'react';
//import { render } from 'react-dom';
//import { Router, Route, hashHistory, RouteHandler } from 'react-router';
//import TosApp from './TosApp';
//
//// read attribute sent via script and convert String into list of cities
//var scriptTag = document.getElementById('myscript');
//var s = scriptTag.getAttribute("data-conf");
////console.log(s);
//var o = JSON.parse(s);
//
//// ParkingListApp properties fed by server
//// #1- filter: {direction, status})
//// #2- schedules: List of available Poitypes as (poitypename)
//
//
//// Config for the app setup TODO - retrieve from server
//var config = {
//  debug: true
//};
//
////render(<App/>, document.getElementById('testDiv'))
//
//let parkingWrapper = () => <ParkingList props={...} />,
//    tosWrapper = () => <TosApp props={...} />,
//    index = () => <div>
//        <header>Some header</header>
//        <RouteHandler />
//        {this.props.children}
//    </div>;
//
//routes = {
//    component: index,
//    path: '/',
//    childRoutes: [
//      {
//        path: 'parkings',
//        component: parkingWrapper
//      }, {
//        path: 'tos',
//        component: tosWrapper
//      }
//    ]
//}
//
//ReactRouter.run(routes, function (Handler) {
//  React.render(<Handler/>, document.body);
//});
//render(<index tos={o['tos']} loggedIn={o['loggedIn'] schedules={o['schedules']} viewfilter={o['filter']} unitname={'A1'} config={config}/>, document.getElementById('testDiv'))
