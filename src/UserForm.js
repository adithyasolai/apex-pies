import { Component } from "react";
import { withRouter } from "react-router-dom";

// import banking_logo from "../resources/sector_icons/banking-sector.png";
// import energy_logo from "../resources/sector_icons/energy-sector.png";
// import health_logo from "../resources/sector_icons/health-sector.png";
// import tech_logo from "../resources/sector_icons/tech-sector.png";

const SECTORS = ["Tech", "Health", "Energy", "Banking"];

class UserForm extends Component {
  constructor() {
    super();

    var userID = "DummyUser" + parseInt(Math.random() * 1000);
    this.state = {
      age: 18, // lowest possible age to invest is 18
      risk: 1, // ranges from 1-10
      sector: "Tech", // no sector selected at the beginning.
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
      return (
        <div className="userForm">
          <form
            onSubmit={this.handleSubmit.bind(this)}
          >
            {/* missing htmlFor */}
          
            <h1><p className="p">Pie Calculator</p></h1>
            
            <h2><p className="p">Welcome to APEX Pie Calculator. Input your age, risk tolerance, and primary sector to receive a diverse pie of stocks. Hover above any input to learn how each factor affects the stocks you should invest in.</p></h2>
            
            <label > 
            <span className="hovertext" data-hover="Generally speaking, the younger an investor is, the riskier their portfolio can be. This is due to the fact they probably will not be withdrawing their money for years and therefore have much more time to recover and recoup from any losses. The higher the risk of a portfolio, the higher its beta.">
              Age
               </span>
            <div/>

            <div class="slidecontainer">
              <input onChange={(e) => this.setState({ age: e.target.value })} type="range" min="18" max="75" 
              value={this.state.age} class="slider" id="myRange"></input>
              <p>{this.state.age}</p>
            </div>
            </label>
  
            <br/>
            <br/>
            <label> 
            <span className="hovertext" data-hover="The amount of risk an investor takes on depends on several other factors besides age. An investor should also take into account their existing debt, savings account balance, and net worth. An investor with low debt combined with high savings account balance and net worth would have a higher risk tolerance.">
              Risk Tolerance
               </span>
               <div/>
               <div class="slidecontainer">
                    <input onChange={(e) => this.setState({ risk: e.target.value })} type="range" min="1" max="10" 
                    value={this.state.risk} class="slider" id="myRange"></input>
                    <p>{this.state.risk}</p>
              </div>
            </label>

            <br/>
            <br/>

            <label>
            <span className="hovertext" data-hover="Sectors are very different from each other in terms of risk and return. In general, when compared to Tech and Energy, Banking and Healthcare tend to be less riskier sectors, which means that they typically have a lower return. ">
              Sector of Interest
              <div/>
              </span>
              <select
                value={this.state.sector}
                onChange={(e) => this.setState({sector: e.target.value}) } 
                onBlur={(e) => this.setState({sector: e.target.value})} // this is just here for accessibility for disabled people that use screenreaders.
              >
                {/* empty option */}

                All sectors
                {
                  SECTORS.map((s) => (
                    <option value={s} key={s}>
                      {s}
                    </option>
                  ))
                }

              </select>

            </label>
           

            <br/>
            <br/>
            <button className = "button glow-button">Submit</button>
            
          
          </form>

        </div>
        
      )
    
    }
  }

const UserFormWithRouter = withRouter(UserForm);

export default UserFormWithRouter;
