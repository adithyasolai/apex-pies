import { Component } from "react";
import Collapsible from "react-collapsible";

class ResourcesFaq extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      <div>
        <h1> Resources/FAQs</h1>

        <Collapsible
          trigger="What is Apex Fund?"
          triggerClassName="collapsible"
          triggerOpenedClassName="collapsible"
        >
          <p className="content">
            {" "}
            The Apex Fund is a student fund with ~$7.5K in AUM with a focus on
            high-quality, FCF generative small to mid-cap businesses. We
            evaluate businesses with fundamental research and derive support
            from underlying thematic trends, data science models, and market
            timing strategies to generate and maximize α.
          </p>
        </Collapsible>

        <br />

        <Collapsible
          trigger="Why is diversification important?"
          triggerClassName="collapsible"
          triggerOpenedClassName="collapsible"
        >
          <p className="content">
            {" "}
            Diversification is a technique that reduces risk by allocating
            investments among various financial instruments, industries and
            other categories. It aims to maximize return by investing in
            different areas that should each react differently to changes in
            market conditions.
          </p>
        </Collapsible>

        <br />

        <Collapsible
          trigger="What makes a stock risky?"
          triggerClassName="collapsible"
          triggerOpenedClassName="collapsible"
        >
          <p className="content">
            {" "}
            A stock is considered risky when it does not have a lot of earnings
            history. This is important because it proves to investors that the
            company has a history of generating cash for the business. Another
            aspect that makes a stock risky is the lack of time on the market.
            If the stock has recently gone public, it will be more volatile due
            to investors not knowing how the stock should be valued.
          </p>
        </Collapsible>

        <br />

        <Collapsible
          trigger="What is the S&P 500?"
          triggerClassName="collapsible"
          triggerOpenedClassName="collapsible"
        >
          <p className="content">
            {" "}
            The Standard and Poor's 500, or simply the S&P 500, is a stock
            market index tracking the performance of 500 large companies listed
            on stock exchanges in the United States. It is one of the most
            commonly followed equity indices
          </p>
        </Collapsible>

        <br />

        <Collapsible
          trigger="Resources"
          triggerClassName="collapsible"
          triggerOpenedClassName="collapsible"
        >
          <p className="content">
            {" "}
            https://www.youtube.com/watch?v=bJHr6_skXWc <br />{" "}
            https://www.youtube.com/watch?v=Pmlsa5-ruMk
            <br /> https://www.youtube.com/watch?v=4gn4F1VmTvM{" "}
          </p>
        </Collapsible>
      </div>
    );
  }
}

export default ResourcesFaq;
