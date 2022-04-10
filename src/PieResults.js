import { Component } from "react";
import { withRouter } from "react-router-dom";

class PieResults extends Component {
  constructor() {
    super();

    this.state = { loading: true };
  }

  async componentDidMount() {
    try{
      const response = await fetch("http://localhost:5000/fetchpies", {
                                    method: "POST",
                                    headers: {
                                      "Content-Type": "application/json",
                                    },
                                    body: JSON.stringify({ userId: this.props.location.state.userId }),
                                  })

      const json = await response.json()
      
      console.log(json.avgBeta)
      console.log(json.pie)
      // .then(data => {console.log(data); this.setState({pieData: data})});

      this.setState(
        // a fast way of just putting all the API's return values into the state of this component instead of manually typing out
        // each field (name, image, breed, location, etc.)
        Object.assign(
          {
            loading: false,
            avgBeta: (Math.round(json.avgBeta * 100) / 100).toFixed(2) ,
            pie: json.pie
          }
        )
      );

    } catch (err) {
      console.log(err)
    }

    
  }

  render() {
    if (this.state.loading) {
      return <h2>loading ...</h2>;
    }
    const age = this.props.location.state.age;
    const risk = this.props.location.state.risk;
    const sector = this.props.location.state.sector;
    const userId = this.props.location.state.userId;
    console.log(this.state)

    const numStocks = Object.keys( this.state.pie).length;
    console.log("Number stocks", numStocks)

    const lineBreak = <br/>;

    return (
      <div>
        <h1>
          Age: {age} -- Risk: {risk} -- Sector: {sector} -- User ID: {userId}
        </h1>

        <p> Overall Beta of Pie: {this.state.avgBeta} </p>

        {

          Array.from(Array(numStocks), (x, i) => i).map((stockIndex) => 
          {
            return (<p key={stockIndex}>
                      Percentage: {this.state.pie[stockIndex]["Percentage"]}
                      
                      {lineBreak}

                      Sector: {this.state.pie[stockIndex]["Sector"]}

                      {lineBreak}

                      Ticker: {this.state.pie[stockIndex]["Ticker"]}

                    </p>);
          })
        }

        <br/>
      </div>
    );
  }
}

const PieResultsWithRouter = withRouter(PieResults);

export default PieResultsWithRouter;