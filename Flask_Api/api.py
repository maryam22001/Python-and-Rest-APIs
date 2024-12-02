from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource ,Api,reqparse,fields,marshal_with,abort
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

db=SQLAlchemy(app)
api =Api(app)
#Shape the data
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

##REPRESENTATION OF THE DATA AS A STRING
    def __repr__ (self):
                   return f"User( name= {self.name},email= {self.email})"

##ReqParse:define arguments that supposed to come in whan you want to 
# send data to our api and create new data we need to validate this 

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name is required")
user_args.add_argument("email", type=str, required=True, help="Email is required")

userFields={
       
       'id':fields.Integer,
       'name':fields.String,
       'email':fields.String,
}




#marsher_with is adecorater and it helps us send the json file in 
#a serialized format

class Users(Resource):
       @marshal_with(userFields) 
       def get(self):
              users = UserModel.query.all()
              return users

#post request function to test the db 
       @marshal_with(userFields) 
       def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users,201

#what if I want to ubdate 1user or delete it 
class User(Resource):
      @marshal_with(userFields)
      def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
      @marshal_with(userFields)
      def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user 
    
      @marshal_with(userFields)
      def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


api.add_resource(Users, '/api/users/' )
api.add_resource(Users, '/api/users/<int:id>' )




@app.route('/') ##send back a simple webpagedata 


#the function that runs after the route
def home ():
    return '<h1>Flask Rest API</h1>'
if __name__ == '__main__':
    app.run(debug=True) ;# it is good to have debug = true in development not in production
