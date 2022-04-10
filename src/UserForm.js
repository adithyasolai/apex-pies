import { Component } from "react";
import { withRouter } from "react-router-dom";

const SECTORS = ["Tech", "Health", "Energy", "Banking"];

class UserForm extends Component {
  constructor() {
    super();

    var userID = "DummyUser" + parseInt(Math.random() * 1000);
    this.state = {
      age: 18, // lowest possible age to invest is 18
      risk: 1, // ranges from 1-10
      sector: "", // no sector selected at the beginning.
      userId: userID // filled in later and sent to PieResults page to fetch pies from BackEnd
    };
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log(JSON.stringify(this.state));

    fetch('http://localhost:5000/', {
      method: 'POST',
      headers : {
        'Content-Type':'application/json'
      },
      body: JSON.stringify(this.state)
    })

    this.props.history.push({
      pathname: '/pieresults',
      state: this.state
    })

  }

  render() {
    console.log("Current Age Value: ", this.state.age); 
    console.log("Current Risk Tolerance Value: ", this.state.risk); 
    console.log("Current Sector Selected: ", this.state.sector); 
    console.log("Current UserID: ", this.state.userId); 
    return (
      <div className="userForm">
        <form
          onSubmit={this.handleSubmit.bind(this)}
        >
          {/* missing htmlFor */}
          <label> 
            Age: 
            <select
              value={this.state.age}
              onChange={(e) => this.setState({age: e.target.value})} 
              onBlur={(e) => this.setState({age: e.target.value})} // this is just here for accessibility for disabled people that use screenreaders.
            >
              {/* empty option */}
              <option/> 

              {/* 18-74 */}
              {
                Array.from(Array(57),(x,i)=>i+18).map((ageNum) => (
                  <option value={ageNum} key={ageNum}>
                    {ageNum}
                  </option>
                ))
              }

              {/* 75 internally, but displayed as "75+" */}
              <option value={75}>
                75+
              </option>

            </select>
          </label>

          <label> 
            Risk Tolerance: 
            <select
              value={this.state.risk}
              onChange={(e) => this.setState({risk: e.target.value})} 
              onBlur={(e) => this.setState({risk: e.target.value})} // this is just here for accessibility for disabled people that use screenreaders.
            >
              {/* empty option */}
              <option/> 

              {/* 1-10 */}
              {
                Array.from(Array(10),(x,i)=>i+1).map((riskNum) => (
                  <option value={riskNum} key={riskNum}>
                    {riskNum}
                  </option>
                ))
              }

            </select>
          </label>

          <label>
            Sector of Interest
            <select
              value={this.state.sector}
              onChange={(e) => this.setState({sector: e.target.value}) } 
              onBlur={(e) => this.setState({sector: e.target.value})} // this is just here for accessibility for disabled people that use screenreaders.
            >
              {/* empty option */}
              <option/> 

              {/* All sectors */}
              {
                SECTORS.map((s) => (
                  <option value={s} key={s}>
                    {s}
                  </option>
                ))
              }

            </select>

          </label>
          
          </form>

        </div>
        
      )
    
    }
  }

  const UserFormWithRouter = withRouter(UserForm);

  export default UserFormWithRouter;