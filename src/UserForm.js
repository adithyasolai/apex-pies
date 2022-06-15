/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */
/* eslint-disable jsx-a11y/click-events-have-key-events */
import { withRouter } from "react-router-dom";
import { Link } from "react-router-dom";

import banking_logo from "../resources/sector_icons/banking-sector.jpeg";
import energy_logo from "../resources/sector_icons/energy-sector.jpeg";
import health_logo from "../resources/sector_icons/health-sector.jpeg";
import tech_logo from "../resources/sector_icons/tech-sector.jpeg";

import {useAuth} from './contexts/AuthContext'
import { useState } from "react";
import { useHistory } from 'react-router-dom';

const SECTORS = ["Technology", "Health Care", "Energy ", "Banking"];
const SECTOR_IMAGES = [tech_logo, health_logo, energy_logo, banking_logo];
const SECTOR_HOVER_INFO = [
  "Tech: These companies have a high beta and volatility. The technology sector is often one of the most attractive growth investments in an economy. Tech stocks have higher betas than the market, hence the presumed risk. If beta is greater than 1.0 then price swings are larger than the market over time. If beta is less than 1.0 then the stock has less risk and offers lower returns. Investors looking to benefit from intraday price changes and short-term momentum strategies usually pick high beta securities.",
  "Healthcare: These companies have a low beta and volatility. However, users should be cautious of government intervention and principal-agent problems. Positive long-term demographics trends, including an aging global population and a growing middle class in emerging markets. Return in demand for elective procedures, drug sales, medical equipment and diagnostics",
  "Energy: These companies have a high beta and volatility. It is subject to risks such as economic activity level, weather, and environmental regulations. They have potential for high dividends or company growth.",
  "Banking: Financial companies have a low beta and volatility. The banking sector pays dividends, which demonstrates a great history and provides investors with a share in profits. Value investors are drawn to bank stocks, which are the most susceptible to emotional short-term forces given the leverage and nature of the business.",
];
const NUM_SECTORS = SECTORS.length;

import React from 'react'

const UserForm = () => {
  const {currentUser} = useAuth();
  const [age, setAge] = useState(18);
  const [risk, setRisk] = useState(1);
  const [sector, setSector] = useState("Technology");
  const [activeSectorImageIndex, setActiveSectorImageIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  // Handler for when the user clicks Submit and requests a diversified Pie based on their inputs.
  // A loading screen should show in the front-end immediately after the Submit button is clicked.
  // The loading screen should stay until the backend server confirms that the new Pie has been
  // calculated and stored in the Firebase DB.
  // Once the backend server gives this confirmation, we will serve the PieResults page, which
  // will show another loading screen until the Plotly chart is fetched from the backend.
  async function handleSubmit(event) {
    // Show "Creating Your Pie ..." screen while waiting for Pie to be published to DB
    setLoading(true)

    event.preventDefault();

    // Send request to backend server to calculate a diversified Pie
    // for the user's selected inputs (age, risk tolerance, and sector).
    // Wait for the request to finish.
    await fetch("http://localhost:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(this.state),
    });

    // Move to the PieResults page after confirming that backend server finished making Pie.
    // Also sends the current state as props to the PieResults page so that
    // the PieResults page has access to the user's selected inputs.
    history.push({location: "/pieresults", state: this.state})
  }

  // Loading screen that is shown immediately after the user clicks Submit button.
  if (loading) {
    return <h2>Creating your Pie ...</h2>;
  }

  console.log("Current Age Value: ", age);
  console.log("Current Risk Tolerance Value: ", risk);
  console.log("Current Sector Selected: ", sector);

  return (
    <div className="userForm">
      <form onSubmit={handleSubmit}>
        {/* missing htmlFor */}

        {/* Title */}
        <h1>
          <p className="p">Apex Portfolio Calculator</p>
        </h1>

        {/* Introductory Text */}
        <h4>
          <p className="p">
            An Introduction to Investing & Financial Literacy
          </p>
        </h4>
        <h2>
          <p className="p">
            Welcome to the Apex Pies Calculator! This app is intended for
            people that are looking to start investing, but don’t know where
            to start. Don’t worry, we’re here to help! Input your age, your
            risk tolerance, and what industry you’d like to invest in the
            most.
          </p>
        </h2>

        {/* Age Slider */}
        <label>
          <span
            className="hovertext"
            data-hover="The younger an investor is, the riskier the portfolio should be. The rationale behind this logic is because these investors have more time until they need to cash out their investments. There are always ups and downs when investing, and having higher risk generally guarantees higher returns in the long run."
          >
            Age
          </span>
          <div />

          <div className="slidecontainer">
            <input
              onChange={(e) => setAge(e.target.value) }
              type="range"
              min="18"
              max="75"
              value={age}
              className="slider"
              id="myRange"
            ></input>
            <p>{age + " years old"}</p>
          </div>
        </label>

        <br />
        <br />

        {/* Risk Tolerance Slider */}
        <label>
          <span
            className="hovertext"
            data-hover="The amount of risk an investor takes on depends on several factors. The factors investors should take into account include: their existing debt, savings account balance, and net worth. For example: An investor with low debt combined with high savings account balance and net worth would have a higher risk tolerance."
          >
            Risk Tolerance
          </span>
          <div />
          <div className="slidecontainer">
            <input
              onChange={(e) => setRisk(e.target.value)}
              type="range"
              min="1"
              max="10"
              value={risk}
              className="slider"
              id="myRange"
            ></input>
            <p>{risk}</p>
          </div>
        </label>

        <br />

        {/* Sector of Interest Hoverable Text */}
        <span
          className="hovertext"
          data-hover="Each sector can provide vastly different returns and have varying levels of risk. Tech and Energy are considered to be high-return, high-risk sectors. Inversely, Banking and Healthcare tend to be less riskier sectors, meaning lower returns. "
        >
          Sector of Interest
        </span>

        <br/>

        {/* Display currently-selected sector. */}
        <p> {sector} </p>

        {/* Sector of Interest Buttons */}
        <div>
          {Array.from(Array(NUM_SECTORS), (x, i) => i).map((i) => {
            const borderStyle = i == activeSectorImageIndex ? "5px solid #ff0000": "5px solid #95bfd0ff";
            return (
              // the below should be a button, and not an image. (so that screen-readers can read it, and it will be more accesible.)
              // eslint-disable-next-line
              <span
                key={SECTOR_IMAGES[i]}
                className="hovertext_image"
                data-hover={SECTOR_HOVER_INFO[i]}
              >
                <img
                  className="sector_images glow-sectorimage"
                  key={SECTOR_IMAGES[i]}
                  src={SECTOR_IMAGES[i]}
                  data-index={i}
                  onClick={(event) => {
                    const sectorIndex = +event.target.dataset.index;
                    setActiveSectorImageIndex(sectorIndex)
                    setSector(SECTORS[sectorIndex])
                  }} // bind gives the click handler function context about what `this` is to access the state.
                  alt="asdf"
                  style={{border : borderStyle}}
                />
              </span>
            );
          })}
        </div>

        <br />

        <button className="button glow-button">Submit</button>
      </form>

      <br />

      <h3>
        Current User: {currentUser ? currentUser['email'] : currentUser}
      </h3>

      <br />

      <Link to={`/profile`}>
        <button className="button glow-button">View Profile</button>
      </Link>

      <br />
      <br />

      <Link to={`/resourcesfaq`}>
        <button className="button glow-button">Resources and FAQ</button>
      </Link>

    </div>
  );
}

const UserFormWithRouter = withRouter(UserForm);

export default UserFormWithRouter;
