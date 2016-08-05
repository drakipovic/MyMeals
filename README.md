# MyMeals

Simple application for tracking daily meals built using flask as backend(REST API) and React on frontend.
You can see it at http://46.101.25.187

##Installation

Run 
    pip install -r requirements.txt 
to get python depenedencies

Run 
    npm install 
to get frontend dependencies


##Starting server

    python run.py

and head to localhost:5000


###API endpoints
/api/meals - retrieving current user meals

/api/users - all users(this action can be done only by admin or user_manager)

/api/users/<username> - all meals by user with <username>, can be done only by admin

All API endpoints are protected by user roles and can be used only inside the application.
