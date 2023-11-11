from flask import Flask,jsonify,request
from flask_restful import Resource,Api
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson import ObjectId


app = Flask(__name__)
api=Api(app)


client=MongoClient("mongodb+srv://Affanmd:AffanMd@cluster0.fem0x.mongodb.net/?retryWrites=true&w=majority")
db=client["corider"]
usersList=db.users
check=usersList.find({"name":"rohan"})
for post in usersList.find({"name": "rohan"}):
    print(post)
print("started")
#request for get all users
class GetUser(Resource):
    def get(self):
        allUser=[]
        for user in usersList.find():
            allUser.append({'id':str(user['_id']),'name':user['name']})
        return  jsonify(allUser)

#request for get single user by id    
class GetSingleUser(Resource):    
    def get(self,id):
        if ObjectId.is_valid(id): 
           user=usersList.find_one({"_id":ObjectId(id)})
           if user:
              return jsonify({'id':str(user['_id']),'name':user['name'],'email':user['email'],'password':user['password']})
           return {'error':'user not found'},404 
        return {'error':'user id not valid'},4
#request for post user by id reference
class PostUser(Resource):
    def post(self):
       newUser={'name':request.json['name'],'email':request.json['email'],'password':generate_password_hash(request.json['password'])}
       checkEmail=usersList.find_one({"email":newUser['email']})
       if checkEmail:
        return {'msg':'email already exist'}
            
       usersList.insert_one(newUser)
       return {'msg':'data added success'}

#request for updating user by id reference   
class UpdateUser(Resource):
    def put(self,id):
      if ObjectId.is_valid(id):  
        checkId=usersList.find_one({"_id":ObjectId(id)})
        if checkId:
          newUser={'name':request.json['name'],'email':request.json['email'],'password':generate_password_hash(request.json['password'])}    
          checkEmail=usersList.find_one({"email":newUser['email']})
          if not checkEmail:
              filter={'_id':ObjectId(id)}
              newInfo={"$set":newUser}
              usersList.update_one(filter,newInfo)
              return {'msg':'user updated successfully'}
          else:
              return {'msg':'email already exist'} 
        return {'error':'user  not found'},404 
      return {'error':'user id not valid'}
       
   
#request for deleting user by id reference   
class DelelteUser(Resource):
    def delete(self,id):
        if ObjectId.is_valid(id):
           checkId=usersList.find_one({"_id":ObjectId(id)})
           if checkId: 
             userDel=usersList.delete_one({'_id':ObjectId(id)})
             if userDel.deleted_count==1:
               return {'msg':'user deleted successfully'}
           else:
               return {'error':'user not found'},404
        else:
            return {'error' :'user id not valid'}
               

#end points definations
api.add_resource(GetUser,'/user')
api.add_resource(GetSingleUser,'/user/<string:id>')
api.add_resource(PostUser,'/user')
api.add_resource(UpdateUser,'/user/<string:id>')
api.add_resource(DelelteUser,'/user/<string:id>')


if __name__ =='__main__':
    app.run(host="0.0.0.0",port=5000)
