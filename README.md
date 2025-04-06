
**Back end for African cultural exchange platform**
This platform allows users from different cultures or regions to share unique knowledge, experiences, and traditions. The idea is to connect people across our continent and encourage learning about each other's cultures, languages, food, festivals, arts, and history.

**Key Features:**

**User Registration and Authentication**
- Sign Up: Users can register for an account.
- Login: Users can log in to their account.
- Logout: Users can log out.
- User Profiles: Each user has a profile where they can manage their information and posts.

**Cultural Knowledge Sharing:**
- Users can create posts about various aspects of their culture: food recipes, traditional clothing, folklore, language lessons, etc.
- Liking posts
- Commenting on posts

**Events:**
- Users can organize cultural events (e.g., cooking classes, cultural tours, language exchange meetings) and invite other users to participate, and users can schoose which events to attend to and also leave an event when desired.
- Events could include details like time, location, and a description of the cultural activity.
- View their own posts/events through dashboard

**Future plan:**
This project is aimed to grow in a great scale for the future by including features like chat, zoom events, following eachother, event recommendation according to who they follow and past attending patterns etc

**Endpoints:**
  🧍 Users
  - Register
    POST /register/


    Request Body:
  
  
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "FirstName": "string",
      "LastName": "string"
    }

- Login

  POST /login_/

  Returns auth token and user id

- Profile

  GET /mydashboard/pk/

  PUT /edituser/pk/ (Update user info)



📸 Posts

  - List Posts

    GET /feed_/


    Pagination supported (?page=1)


  - Create Post
  
    POST /addpost/

    Fields: Title, content, image


  - Detail
  - 
    GET /post/pk

  - /Update/Delete

    PUT /edit_post/pk


    DELETE /edit_post/pk



  📅 Events
  
  - List Events
  
    GET /event/


    Pagination supported


  - Create Event
  
    POST /newevent/


    Fields: title, description, date_time, creator


  - Detail View
  
    GET /viewevent/pk



  🧾 Media
  
  - Uploaded media files are accessible via:


  - /media/<filename>
  
    Make sure media is properly configured on the server.
  

- Pagination
  
  All list endpoints use page number pagination.
  Example:
  
  
  GET /feed_/?page=2


- Status Codes
  
  200 OK – Success
  
  
  201 Created – Resource created
  
  
  400 Bad Request – Validation error
  
  
  401 Unauthorized – Token missing or invalid
  
  
  404 Not Found – Resource doesn’t exist



**Notes:**

  CORS is enabled for all origins in development.
  
  
  Ensure static and media files are served correctly in production.
  
  
  
  Contact
  For any issues or improvements, please contact me at @ephrem007 on telegram or discord

✨ Thank you for using the African Cultural Exchange Platform!


