import React, { Component } from "react";
import "./style.css";
import AutosizeInput from "react-input-autosize";
import IngredientItem from "./components/IngredientItem";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchText: "",
      showResults: false,
      ingredientItems: []
    };
  }

  /**
   * Called when the text box's text is changed to update the app state with the new text.
   */
  updateInputValue = (input, event) => {
    /* New state is merged with existing state */
    const newState = {
      searchText: event.target.value
    };
    this.setState(newState);
  };

  /**
   * Called when there is a key press in the text box.
   */
  handleKeyPress = async event => {
    if (event.key === "Enter") {
      const response = await fetch('https://5ab0bedng2.execute-api.eu-west-2.amazonaws.com/test/recipes/'+this.state.searchText);
      const recipe = await response.json(); //extract JSON from the http response

      /* Create IngredientItem components for each ingredient */
      var ingredientResults = recipe.ingredients
      const ingredientItems = ingredientResults.map(ingredient => (
        <IngredientItem text={ingredient} />
      ));

      /* New state is merged with existing state */
      const newState = {
        ingredientItems: ingredientItems,
        showResults: true
      };
      this.setState(newState);
    }
  };

  render() {
    return (
      <div className="root-div">
        <div className="search-div">
          <h1 className="search-text">What's in </h1>
          {/* https://github.com/JedWatson/react-input-autosize */}
          <AutosizeInput
            name="search-text"
            placeholder="   "
            value={this.state.searchText}
            onChange={this.updateInputValue.bind(this, "searchText")}
            onKeyPress={this.handleKeyPress}
            inputStyle={{
              fontFamily: "MontserratBold",
              fontSize: "4vw",
              /* Input text color */
              color: "#696969",
              /* Input text is the same height as the header text */
              marginTop: "0.3vw",
              /* Input text as a line */
              background: "transparent",
              border: "none",
              borderBottom: "0.3vw solid black"
            }}
          />
          <h1 className="search-text">?</h1>
        </div>
        {/* Only display results once a recipe has been searched for */}
        {this.state.showResults ? (
          <div className="results-div">{this.state.ingredientItems}</div>
        ) : null}
      </div>
    );
  }
}

export default App;
