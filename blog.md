# HTTP_Request
## For a blog application, different parts of the system will require different HTTP requests to handle functionalities like user authentication, creating posts, managing comments, and more. Here’s a breakdown of the necessary HTTP requests for different parts of the application:

## 1.  User Authentication (Auth):
- ### Login/logout, Registration, Tokens:
    * **Http Method:** *POST*
- ### view profile
    * **Http Method:** *Get*
- ### Update profile
    * **Http Method:** *PUT/PATCH*

## 2. Blog Posts:
- ### Create Post
    * **Http Method:** *POST*
- ### Get post
    * **Http Method:** *Get*
- ### Upload post
    * **Http Method:** *PUT/PATCH*
- ### Delete post
    * **Http Method:** *Delete*

## 3. Comments
- ### Add comment
    * **Http Method:** *POST*
- ### Edit comment
    * **Http Method:** *PUT/PATCH*
- ### See comments
    * **Http Method:** *Get*
- ### Delete comment
    * **Http Method:** *Delete*

## 4.  Likes:
- ### Liking a post
    * **Http Method:** *POST*
- ### Unliking a post
    * **Http Method:** *DELETE*


## 5.  Admin:
- ### Get All Users
    * **Http Method:** *Get*
- ### Ban User
    * **Http Method:** *PATCH*
- ### Delete User
    * **Http Method:** *DELETE*