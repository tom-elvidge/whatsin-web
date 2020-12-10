USE WhatsIn;

-- Recipes --

CREATE TABLE Recipes (
	id VARCHAR(250) PRIMARY KEY NOT NULL,
    title VARCHAR(250) NOT NULL
);

INSERT INTO Recipes VALUES ('pizza', 'Pizza');

-- RecipeIngredients --

CREATE TABLE RecipeIngredients (
	id INT PRIMARY KEY AUTO_INCREMENT,
    recipe_id VARCHAR(250) NOT NULL,
    ingredient VARCHAR(250) NOT NULL
);

INSERT INTO RecipeIngredients VALUES (1, 'pizza', 'passata'), (2, 'pizza', 'mozzarella'), (3, 'pizza', 'dough');