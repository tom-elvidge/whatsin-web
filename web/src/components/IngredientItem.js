import React from "react";
import "../style.css";

function IngredientItem(props) {
  return (
    <div className="ingredient-item-div">
      <p>{props.text}</p>
    </div>
  );
}

export default IngredientItem;
