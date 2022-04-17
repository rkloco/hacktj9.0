import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import pic from './plots/scatter0.png';

function App(props) {
  const [getMessage, setGetMessage] = useState({})

  useEffect(()=>{
    axios.get('http://localhost:5000/flask/hello?name='+props.name).then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])
  var mynum = '4'
//<img src={`data:image/png};base64,${getMessage.data.img}`}></img>
//<h3>{getMessage.data.message}</h3>
  return (
    <div className="App">
      <header className="App-header">
        <p>---------</p>
        <div>{getMessage.status === 200 ? 
          <div>
            <img src={`data:image/png};base64,${getMessage.data.img}`}></img>
            <h3>Your Location's Coordinates: {getMessage.data.message}</h3>
            <h3>When will this location be at risk of tidal disruptions from sea level changes?</h3>
            <h2>Low Risk: {getMessage.data.lowyear}</h2>
            <h2>Medium Risk: {getMessage.data.medyear}</h2>
            <h2>High Risk: {getMessage.data.highyear}</h2>
            <h2>Complete Submersion: {getMessage.data.subyear}</h2>
          </div>
          :
          <h3>LOADING</h3>}
        </div>
        
      </header>
    </div>
  );
}


export default App;
