import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class NameForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    //alert('A name was submitted: ' + this.state.value);
    const cityName = this.state.value
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
      <React.StrictMode>
        <App name={cityName}/>
      </React.StrictMode>
    );
    event.preventDefault();
  }

  render() {
    return (
      <div className="Form-header">
        <form onChange={this.handleChange} onSubmit={this.handleSubmit}>
        <label>
          Enter Address:
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      </div>
    );
  }
}

const nameform = ReactDOM.createRoot(document.getElementById('city'))
nameform.render(
  <React.StrictMode>
    <NameForm />
  </React.StrictMode>
);

//ReactDOM.render(<NameForm />, document.getElementById('city'));
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals



reportWebVitals();
