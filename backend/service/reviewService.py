from pydantic import BaseModel
from errors import internalServerError
import logging as logger
from db.main import Database

class ReviewItem(BaseModel):
    title: str
    stars: int
    description: str
    recipeid: int
    username: str

class ReviewService():
    def __init__(self, db: Database):
        self.Database = db
    
    def insertReview(self, review: ReviewItem):
        print("yes here")
        db = self.Database
        try:
            print(f"INSERT INTO {db.ReviewTable} (userName, recipeID, revTitle, revDesc, stars) values\
                ('{review.username}',{review.recipeid},'{review.title}','{review.description}',{review.stars})")
            result = db.query(f"INSERT INTO {db.ReviewTable} (userName, recipeID, revTitle, revDesc, stars) values\
                ('{review.username}',{review.recipeid},'{review.title}','{review.description}',{review.stars})")
            return {
        **review.dict()
      }
        except Exception as e:
            print(e)


