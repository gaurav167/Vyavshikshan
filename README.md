# Vyavashikshan
This is an online platform for helping youth to make informed decisions on career choices in the vocational sector.
## Tech Stack
### Frontend
HTML5
CSS3
JavaScript (jQuery)
### Backend
Python
Django
PostgreSQL/MongoDB
## Show Stoppers
1. Knowledge Center
1. Artificial Intelligence based course recommendation system & novel machine learning algorithm for career choice prediction
1. Group messaging, Question-answer and blogging platform-enables communication between students and counsellors, NGOs, other students
1. Extensive vernacular language support


## Contribution Instructions for backend : 
 1. Use Django 2.0 or greater. Some features will not work on earlier versions.
 2. Make separate branch for each feature assigned to you. Master branch only contains stable and tested features.
 3. All feature will be integrated via Pull Requests only. A merge will be done after it is reviewed by atleast one member.


## Contribution Instructions for frontend :

### API Documentation :

 #### Responses
 
 All responses are JSON.
 
 I. Success Response :
 
 - Upload/Edit/Delete operation :
 
 {
 'status' : 'success'
 }
 
 - Get operation :
 
 JSON String of requested Data.
 
 II. Failiure Responses :
 
 - BAD REQUEST METHOD :
 
 {
  'error':'Only available via METHOD_NAME.',
  'status_code':'400'
  }
 
  - Invalid data via POST :
  
  {
  'status':'failed',
  'message':'Invalid POST data.'
  }
  
  - No object with given name :
  
  {
  'status':'failed',
  'message':'OBJECT_NAME does not exist.'
  }
  
  - Cannot create required object :
  
  {
  'status':'failed',
  'message':"Couldn't create OBJECT_NAME object"
  }
  
  - Unknown Error :
  
  {
  'status':'failed',
  'message':'None'
  }
  
  - Not Fount :
  
  {
  'error':'ENTITY not Found',
  'status_code':'404'
  }
  
  - Any other Error :
  
  {
  'status':'failed','message':'ERROR_MESSASGE_TO_DISPLAY_DIRECTLY'
  }
  
 #### API ENDPOINTS
 
 - Blog APIs : /blog/
 
  1. Submit a Post : post/submit/
  
   Request Method : POST
   
   Form Data :
   
               author - Name of Author
   
               title - Title of Post
               
               subtitle - Subtitle of Post
               
               text - Post Content
               
               categories - category of post
               
               image - (Optional) Background Image
  
  2. Get all Posts : post/all/
   
   Request Method : GET
   
  3. Edit a Post : post/POST_ID/edit/
   
   Request Method : POST
   
   Form Data :
   
              JSON of updated data
              
  4. Delete a Post : post/POST_ID/delete/
  
   Request Method : DELETE
   
  5. Get a post by Specific ID : post/POST_ID/
  
   Request Method : GET
   
  6. Respond to a Post : post/POST_ID/ACTION_NAME/
  
   Request Method : PUT
   
   Actions Allowed : 'Like', 'Dislike'
   
  7. Get posts by Category name : post/CATEGORY_NAME/
  
   Request Method : GET
   
  8. Submit a new category : category/submit/
  
   Request Method : POST
   
   Form Data :
   
              name - Name of category to be added
              
  9. Get all categories : category/all/
  
   Request Method : GET
   
  10. Respond to a category : category/CATEGORY_ID/ACTION_NAME/
  
   Request Method : PUT
   
   Actions Allowed : 'Like', 'Dislike'
   
  11. Delete a category : /category/CATEGORY_ID/delete/
  
   Request Method : DELETE
