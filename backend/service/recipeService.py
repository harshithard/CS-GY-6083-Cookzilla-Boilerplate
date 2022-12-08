from pydantic import BaseModel
from errors import internalServerError
import logging as logger
from db.main import Database

class InsertTag(BaseModel):
  tags: list

class InsertIngredient(BaseModel):
  ingredient_names: list
  ingredient_metrics: list
  ingredient_quantities: list=[0]

class InsertRecipe(BaseModel):
  title: str
  numServings: int
  postedBy: str = ""

class InsertStep(BaseModel):
  steps: list

class RecipeService():
  def __init__(self, db: Database):
    self.Database = db
    self.ID = 0

  def insertRecipe(self, recipe: InsertRecipe):
    db = self.Database

    try:
      insertResult = db.query(f"INSERT into {db.RecipeTable} (title, numServings, postedBy) \
        values('{recipe.title}',{recipe.numServings},'{recipe.postedBy}')")
      
      self.ID = int(insertResult['insertId'])

      return {
        "recipeID": insertResult['insertId'],
        **recipe.dict()
      }
    except Exception as e:
      logger.error("Unable to insert recipe")
      logger.error(e)
      raise internalServerError.InternalServerError()
  
  def insertIngredient(self, ingredient: InsertIngredient):
    db = self.Database
    try:
      for i in range(len(ingredient.ingredient_names)):
        #print(f"SELECT * FROM {db.Ingredient} WHERE iName='{ingredient.ingredient_names[i]}'")
        result = db.query(f"SELECT * FROM {db.Ingredient} WHERE iName='{ingredient.ingredient_names[i]}'")
        #print(result)
        if len(result['result'])==0:
          #print("\n The ingredient was not found\n")
          link = "https://www.amazon.com/s?k="+ingredient.ingredient_names[i]
          #print(f"INSERT INTO {db.Ingredient} (iName, purchaseLink) values('{ingredient.ingredient_names[i]}','{link}')")
          db.query(f"INSERT INTO {db.Ingredient} (iName, purchaseLink) values('{ingredient.ingredient_names[i]}'\
            ,'{link}')")

        #print(f"INSERT into {db.IngredientTable} (recipeID, iName, unitName, amount) \
        #values({self.ID},'{ingredient.ingredient_names[i]}','{ingredient.ingredient_metrics[i]}',{ingredient.ingredient_quantities[i]})")
        db.query(f"INSERT into {db.IngredientTable} (recipeID, iName, unitName, amount) \
        values({self.ID},'{ingredient.ingredient_names[i]}','{ingredient.ingredient_metrics[i]}',{int(ingredient.ingredient_quantities[i])})")
        #print("itworked!!!!!!!!!!")

        
      return {
        **ingredient.dict()
      }
    except Exception as e:
      logger.error("Unable to insert ingredient")
      logger.error(e)
      raise internalServerError.InternalServerError()

  def insertTag(self, tag: InsertTag):
    db = self.Database
    try:
      for i in range(len(tag.tags)):
        #print(f"INSERT into {db.TagTable} (recipeID, tagText) values('{self.ID}','{tag.tags[i]}')")
        db.query(f"INSERT into {db.TagTable} (recipeID, tagText) values('{self.ID}','{tag.tags[i]}')")
    
      return {
        **tag.dict()
      }

    except Exception as e:
      logger.error("Unable to insert tags")
      logger.error(e)
      raise internalServerError.InternalServerError()

  def insertSteps(self, step: InsertStep):
    db = self.Database
    try:
      for i in range(len(step.steps)):
        print(f"INSERT into {db.StepTable} (StepNo, recipeID, sDesc) \
        values({i+1},{self.ID},'{step.steps[i]}')")
        db.query(f"INSERT into {db.StepTable} (StepNo, recipeID, sDesc) \
        values({i+1},{self.ID},'{step.steps[i]}')")
    
      return {
        **step.dict()
      }

    except Exception as e:
      logger.error("Unable to insert tags")
      logger.error(e)
      raise internalServerError.InternalServerError()