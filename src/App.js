import React, { Component } from "react";
import "./style.css";
import AutosizeInput from "react-input-autosize";
import IngredientItem from "./components/IngredientItem";
import ReactLoading from 'react-loading';

class App extends Component {

  /**
   * Set up state for application.
   * 
   * @param {*} props 
   */
  constructor(props) {
    super(props);
    this.state = {
      searchText: "",
      showResults: false,
      loadingResults: false,
      ingredientItems: []
    };
  }

  /**
   * Generate page to display in browser.
   */
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
        {/* Only display loading spinner whilst searching for a recipe */}
        {this.state.loadingResults ? (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
        }}>
            <ReactLoading type={'spin'} color={'black'} height={'5%'} width={'5%'} />
        </div>
        ) : null}
        {/* Only display results once a recipe has been searched for */}
        {this.state.showResults ? (
          <div className="results-div">{this.state.ingredientItems}</div>
        ) : null}
      </div>
    );
  }

  /**
   * Get the text from the search box and update the searchText attribute in state with it's value.
   */
  updateInputValue = (input, event) => {
    // Using set state merges the passed state with the existing state.
    this.setState({searchText: event.target.value});
  };

  /**
   * Called when Enter is pressed in the search box. Search for the recipe.
   */
  async search() {
    // Display loading animation and hide any existing results.
    this.setState({loadingResults: true, showResults: false});

    // Get recipe with name searchText.
    const axios = require("axios");
    var resp;
    // If failed gets set to true then something went wrong, handle it in the user interface.
    var failed = false;

    try {
      // Attempt to get recipe.
      resp = await axios.get('https://wk0hcgjyi6.execute-api.eu-west-2.amazonaws.com/Prod/whatsin/'+this.state.searchText);
      // resp = await axios.get('http://127.0.0.1:3000/whatsin/'+this.state.searchText);
      console.log(resp)
    } catch (error) {
      // Log error.
      failed = true;
    }

    // Stop the loading animation.
    this.setState({loadingResults: false});

    // Get the ingredients from the response.
    var ingredients;
    if (failed) {
      // If something went wrong getting the recipe then just display an error message.
      ingredients = ['Failed to get recipe']
    } else {
      ingredients = resp.data.ingredients
    }

    // Create IngredientItem components for each ingredient.
    const ingredientItems = ingredients.map(ingredient => (
      <IngredientItem text={ingredient} />
    ));

    // Add the ingedientItems to the state and show the results.
    this.setState({ingredientItems: ingredientItems, showResults: true});
  }

  /**
   * Called when there is a key press in the text box.
   */
  handleKeyPress = event => {
    if (event.key === "Enter") {
      this.search();
    }
  };

}

export default App;
