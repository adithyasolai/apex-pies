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
            <html>
            <head>
            </head>
          
            <h1><p class="p">Pie Calculator</p></h1>
            
            <h2><p class="p">Welcome to APEX Pie Calculator. Input your age, risk tolerance, and primary sector to receive a diverse pie of stocks. Hover above any input to learn how each factor affects the stocks you should invest in.</p></h2>
            
            
            </html>
            <label > 
            <span class="hovertext" data-hover="Generally speaking, the younger an investor is, the riskier their portfolio can be. This is due to the fact they probably will not be withdrawing their money for years and therefore have much more time to recover and recoup from any losses. The higher the risk of a portfolio, the higher its beta.">
              Age
               </span>
            <div/>

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
  
            <br/>
            <br/>
            <label> 
            <span class="hovertext" data-hover="The amount of risk an investor takes on depends on several other factors besides age. An investor should also take into account their existing debt, savings account balance, and net worth. An investor with low debt combined with high savings account balance and net worth would have a higher risk tolerance.">
              Risk Tolerance
               </span>
               <div/>
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

            <br/>
            <br/>

            <label>
            <span class="hovertext" data-hover="Sectors are very different from each other in terms of risk and return. In general, when compared to Tech and Energy, Banking and Healthcare tend to be less riskier sectors, which means that they typically have a lower return. ">
              Sector of Interest
              <div/>
              </span>
              <select
                value={this.state.sector}
                onChange={(e) => this.setState({sector: e.target.value}) } 
                onBlur={(e) => this.setState({sector: e.target.value})} // this is just here for accessibility for disabled people that use screenreaders.
              >
                {/* empty option */}
                <meta name="viewport" content="width=device-width, initial-scale=1"/>

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
            <a href = "#" class = "button glow-button">Submit</a>
            
          
          </form>

        </div>
        
      )
    
    }
  }
}

const UserFormWithRouter = withRouter(UserForm);

export default UserFormWithRouter;
