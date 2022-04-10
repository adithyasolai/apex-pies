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

    fetch("http://localhost:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(this.state),
    });

    this.props.history.push({
      pathname: "/pieresults",
      state: this.state,
    });
  }

  render() {
    console.log("Current Age Value: ", this.state.age);
    console.log("Current Risk Tolerance Value: ", this.state.risk);
    console.log("Current Sector Selected: ", this.state.sector);
    return (
      <div className="userForm">
        <form onSubmit={this.handleSubmit.bind(this)}>
          {/* missing htmlFor */}
          <label>
            <div className="myDIV">Age (Hover above me for more info!): </div>
            <div className="hide">
              Generally speaking, the younger an investor is, the riskier their
              portfolio can be. This is due to the fact they probably will not
              be withdrawing their money for years and therefore have much more
              time to recover and recoup from any losses. The higher the risk of
              a portfolio, the higher its beta.{" "}
            </div>
            <select
              value={this.state.age}
              onChange={(e) => this.setState({ age: e.target.value })}
              onBlur={(e) => this.setState({ age: e.target.value })} // this is just here for accessibility for disabled people that use screenreaders.
            >
              {/* empty option */}
              <option />

              {/* 18-74 */}
              {Array.from(Array(57), (x, i) => i + 18).map((ageNum) => (
                <option value={ageNum} key={ageNum}>
                  {ageNum}
                </option>
              ))}

              {/* 75 internally, but displayed as "75+" */}
              <option value={75}>75+</option>
            </select>
          </label>

          <br />
          <br />
          <label>
            <div className="myDIV">
              Risk Tolerance (Hover above me for more info!):{" "}
            </div>
            <div className="hide">
              The amount of risk an investor takes on depends on several other
              factors besides age. An investor should also take into account
              their existing debt, savings account balance, and net worth. An
              investor with low debt combined with high savings account balance
              and net worth would have a higher risk tolerance.
            </div>
            <select
              value={this.state.risk}
              onChange={(e) => this.setState({ risk: e.target.value })}
              onBlur={(e) => this.setState({ risk: e.target.value })} // this is just here for accessibility for disabled people that use screenreaders.
            >
              {/* empty option */}
              <option />

              {/* 1-10 */}
              {Array.from(Array(10), (x, i) => i + 1).map((riskNum) => (
                <option value={riskNum} key={riskNum}>
                  {riskNum}
                </option>
              ))}
            </select>
          </label>

          <br />
          <br />
          <br />
          <br />

          <label>
            <div className="myDIV">
              {" "}
              Sector of Interest (Hover above me for more info!):{" "}
            </div>
            <div className="hide">
              Sectors are very different from each other in terms of risk and
              return. In general, when compared to Tech and Energy, Banking and
              Healthcare tend to be less riskier sectors, which means that they
              typically have a lower return.
            </div>
            <select
              value={this.state.sector}
              onChange={(e) => this.setState({ sector: e.target.value })}
              onBlur={(e) => this.setState({ sector: e.target.value })} // this is just here for accessibility for disabled people that use screenreaders.
            >
              {/* empty option */}
              All sectors
              {SECTORS.map((s) => (
                <option value={s} key={s}>
                  {s}
                </option>
              ))}
            </select>
          </label>

          <br />
          <br />
          <br />
          <br />
          <button>Submit</button>
        </form>
      </div>
    );
  }
}

const UserFormWithRouter = withRouter(UserForm);

export default UserFormWithRouter;
