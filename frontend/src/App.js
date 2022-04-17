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
  return (
    <div className="App">
      <header className="App-header">
        <p>Coordinates:</p>
        <div>{getMessage.status === 200 ? 
          <h3>{getMessage.data.message}</h3>
          <img src={`data:image/png};base64,${getMessage.data.img}`}></img>
          :
          <h3>LOADING</h3>}
        </div>
        
      </header>
    </div>
  );
}


export default App;
