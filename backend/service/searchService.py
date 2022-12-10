from pydantic import BaseModel
from errors import internalServerError
import logging as logger
from db.main import Database


class SearchService():
  def __init__(self, db: Database):
    self.Database = db

  def retrieveRecipe(self, searchText, selectedTag, selectedStars):
    db = self.Database
    print(" i m here")

    try:
        print(print("SELECT * from {db.RecipeTable} WHERE title LIKE '%{searchText}%'\
        AND recipeID in\
        ( SELECT recipeID FROM {db.TagTable} WHERE {db.TagTable}.tagText = '{selectedTag}' AND recipeID in (\
            SELECT recipeID FROM {db.ReviewTable} group by(recipeID) HAVING AVG({db.ReviewTable}.stars)>= {selectedStars}\
        )  )"))

        retrieveRecipes = db.query(f"SELECT * from {db.RecipeTable} WHERE title LIKE '%{searchText}%'\
        AND recipeID in\
        ( SELECT recipeID FROM {db.TagTable} WHERE {db.TagTable}.tagText = '{selectedTag}' AND recipeID in (\
            SELECT recipeID FROM {db.ReviewTable} group by(recipeID) HAVING AVG({db.ReviewTable}.stars)>= {selectedStars}\
        )  )")

        print(retrieveRecipes)
        return retrieveRecipes
    except Exception as e:
      logger.error("Unable to insert recipe")
      logger.error(e)
      raise internalServerError.InternalServerError()
  
 