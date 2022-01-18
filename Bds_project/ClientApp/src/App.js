import React, { Component } from 'react';
import { Route } from 'react-router';
import { Layout } from './components/Layout';
import { Home } from './components/Home';
import { Model } from './components/Model';
import { UseModel } from './components/UseModel';

import './custom.css'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";

export default class App extends Component {
  static displayName = App.name;

  render () {
      return (
      <Layout>
        <Route exact path='/' component={Home} />
        <Route path='/trainModel' component={Model} />
        <Route path='/useModel' component={UseModel} />
      </Layout>
    );
  }
}
