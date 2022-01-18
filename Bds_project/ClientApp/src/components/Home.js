import React, { Component } from 'react';
import CSVupload from "./CSVupload";

export class Home extends Component {
  static displayName = Home.name;

  render () {
      return (
      <div>
              <h1>Implementation of the
              one-year mortality model for palliative
care needs assessment</h1>
              <p> <strong>  Authors : </strong>  Matias Vedeler Cerda, Cándido García Rodríguez, Arturo Serrano Moliner </p> 
        <p>Welcome to our single-page application, built with:</p>
        <ul>
          <li><a href='https://get.asp.net/'>ASP.NET Core</a> and <a href='https://msdn.microsoft.com/en-us/library/67ef8sbd.aspx'>C#</a> for cross-platform server-side code</li>
          <li><a href='https://facebook.github.io/react/'>React</a> for client-side code</li>
          <li><a href='http://getbootstrap.com/'>Bootstrap</a> for layout and styling</li>
            </ul>
        <p>Check out </p>
        <ul>
            <li><a href='https://github.com/h582618/Biomedical-Data-science---CDSS'>Github Repository</a> for all the code</li>
            <li><strong>About </strong></li>
            <li><strong>Train the model</strong></li>
            <li><strong>Use the model</strong></li>
        </ul>

          </div>
    );
  }
}
