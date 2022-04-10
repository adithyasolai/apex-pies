import { Component } from "react";
import { withRouter } from "react-router-dom";
import { Link } from "react-router-dom";

import banking_logo from "../resources/sector_icons/banking-sector.jpeg";
import energy_logo from "../resources/sector_icons/energy-sector.jpeg";
import health_logo from "../resources/sector_icons/health-sector.jpeg";
import tech_logo from "../resources/sector_icons/tech-sector.jpeg";

const SECTORS = ["Tech", "Health", "Energy", "Banking"];
const SECTOR_IMAGES = [tech_logo, health_logo, energy_logo, banking_logo]
const SECTOR_HOVER_TEXT = ["Tech", "Health", "Energy", "Banking"]
const NUM_SECTORS=SECTORS.length;

class UserForm extends Component {
  constructor() {
    super();

    var userID = "DummyUser" + parseInt(Math.random() * 1000);
    this.state = {
      age: 18, // lowest possible age to invest is 18
      risk: 1, // ranges from 1-10
      sector: "Tech", // no sector selected at the beginning.
      userId: userID, // filled in later and sent to PieResults page to fetch pies from BackEnd
      activeSectorImageIndex: 0
    };
  }

  handleSectorClick(event) {
    const sectorIndex = +event.target.dataset.index;
    this.setState(
    {
      // make our `active` state field the same as the index of the image that was clicked to change what the main picture is in render()
      // this is just HTML stuff
      // event.target is the <img> tag that was clicked.
      // dataset is anything put into <data-?> tags.
      // the + sign coerces the value to be a number
      activeSectorImageIndex: +event.target.dataset.index,
      sector: SECTORS[sectorIndex]
    }
    );
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
          
            <h1><p className="p">Apex Portfolio Calculator</p></h1>
            <h4><p className="p">An Introduction to Investing & Financial Literacy</p></h4>
            <h2><p className="p">Welcome to the Apex Pies Calculator! This app is intended for people that are looking to start investing, but don’t know where to start. Don’t worry, we’re here to help! Input your age, your risk tolerance, and what industry you’d like to invest in the most.</p></h2>
            
            <label > 
            <span className="hovertext" data-hover="The younger an investor is, the riskier the portfolio should be. The rationale behind this logic is because these investors have more time until they need to cash out their investments. There are always ups and downs when investing, and having higher risk generally guarantees higher returns in the long run.">
              Age
               </span>
            <div/>

              <div className="slidecontainer">
                <input onChange={(e) => this.setState({ age: e.target.value })} type="range" min="18" max="75" 
                value={this.state.age} className="slider" id="myRange"></input>
                <p>{this.state.age +" years old"}</p>
              </div>
            </label>
  
            <br/>
            <br/>
            <label> 
            <span className="hovertext" data-hover="The amount of risk an investor takes on depends on several factors. The factors investors should take into account include: their existing debt, savings account balance, and net worth. For example: An investor with low debt combined with high savings account balance and net worth would have a higher risk tolerance.">
              Risk Tolerance
               </span>
               <div/>
               <div className="slidecontainer">
                    <input onChange={(e) => this.setState({ risk: e.target.value })} type="range" min="1" max="10" 
                    value={this.state.risk} className="slider" id="myRange"></input>
                    <p>{this.state.risk}</p>
              </div>
            </label>

            <br/>
            <br/>

            <label>
            <span className="hovertext" data-hover="Each sector can provide vastly different returns and have varying levels of risk. Tech and Energy are considered to be high-return, high-risk sectors. Inversely, Banking and Healthcare tend to be less riskier sectors, meaning lower returns. ">
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

            <div>
              {Array.from(Array(NUM_SECTORS), (x, i) => i).map((i) =>
              {
                return (
                // the below should be a button, and not an image. (so that screen-readers can read it, and it will be more accesible.)
                // eslint-disable-next-line
                <span className="hovertext_image" data-hover={SECTOR_HOVER_TEXT[i]}>
                <button class = "button_image"><img
                  className = "sector_images"
                  key={SECTOR_IMAGES[i]}
                  src={SECTOR_IMAGES[i]}
                  data-index={i}
                  onClick={this.handleSectorClick.bind(this)} // bind gives the click handler function context about what `this` is to access the state.
                  alt="asdf"
    
                /></button></span>
                )
              }
              )
              }
            </div>
           

            <br/>
            <br/>
            <button className = "button glow-button">Submit</button>
            
          
          </form>

          <Link to={`/resourcesfaq`}>
            <button className = "button glow-button">Resources and FAQ</button>
          </Link>
          

        </div>
        
      )
    
    }
  }

const UserFormWithRouter = withRouter(UserForm);

export default UserFormWithRouter;
