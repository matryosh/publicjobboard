import React from 'react';
import { ThemeProvider, CSSReset } from "@chakra-ui/core";
//import './App.css';
import { Link, Redirect, Route, Switch } from 'react-router-dom';
import Prelaunch from './components/Prelaunch';

function App() {
  return (
    <ThemeProvider>
      <CSSReset />
      <Switch>
        <Route exact path='/'>
          <Prelaunch />
        </Route>
      </Switch>
      
    </ThemeProvider>
    
  );
}

export default App;
