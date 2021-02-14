import React, { useEffect } from 'react';
import Cookies from 'universal-cookie';
import { useDispatch } from 'react-redux';
import NavBar from './components/NavBar';
import Home from './components/Home';
import Landing from './components/Landing';
import DateSelecter from './components/DateSelecter';
import Monthelecter from './components/MonthSelecter';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {
  // const cookies = new Cookies();
  // const dispatch = useDispatch();
  // useEffect(() => {
  //   // dispatch to redux setting the user
  //   if (cookies.get('user')) {
  //     dispatch(setUser(cookies.get('user')));
  //   }
  // }, [cookies, dispatch]);

  return (
    <Router>
      <div className="App">
        <NavBar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/landing" component={Landing} />
          <Route exact path="/calendar" component={DateSelecter} />
          <Route exact path="/month_picker" component={Monthelecter} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
