from flask import  request, make_response
from flask_restx import Namespace, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import UserModel
from app import db, es
import re

auth = Namespace('Auth', description='Authentication')
auth.authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}
auth.security='apikey' 


@auth.route("/signup", methods=["POST"])
class SignUp(Resource):
    @auth.doc(responses={ 201: 'Created', 202: 'User already exists. Please Log in.' })
    @auth.doc(parser = auth.parser()
                .add_argument('name', type=str, required=True, help='Name', location='form')
                .add_argument('email', type=str, required=True, help='Email address', location='form')
                .add_argument('password', type=str, required=True, help='Password', location='form'))
    def post(self):
        data = request.form
        name, email, password = data['name'], data['email'].lower(), data['password']
        
        if not re.match(r"^[a-zA-Z ]+$", name):
            return make_response('Invalid name', 400)
        if not re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", email):
            return make_response('Invalid email address', 400)
        if len(password) < 8:
            return make_response('Password should be atleast 8 characters', 400)
        
        user = UserModel.query.filter_by(email=email).first()
        print(data, email, password, user)
        if user:
            return make_response('User already exists. Please Log in.', 202)
        user = UserModel(
            name = name, 
            email = email, 
            password = generate_password_hash(password, method='sha256')
            # password = password
        )
        db.session.add(user)
        db.session.commit()
        return make_response('Successfully registered.', 201)


@auth.route('/login', methods=['POST']) 
class LogIn(Resource):
    @auth.doc(responses={ 200: 'Success', 401: 'Could not verify' })
    @auth.doc(parser = auth.parser()
            .add_argument('email', type=str, required=True, help='Email address', location='form')
            .add_argument('password', type=str, required=True, help='Password', location='form')
    )
    def post(self):
        auth = request.authorization
        data = request.form
        email, password = data['email'], data['password']  
        if auth:
            email, password = auth.email, auth.password
        if not email or not password: 
            return make_response('Could not verify', 401, {'Authentication': 'Credentials required"'})   
        if not re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", email):
            return make_response('Invalid email address', 400)
        if len(password) < 8:
            return make_response('Password should be atleast 8 characters', 400)
        
        user = UserModel.query.filter_by(email=email).first()  
        if not user: 
            return make_response('Could not verify', 401, {'Authentication': 'Invalid Email Address."'})   
        
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            return {'access_token': access_token}, 200
        
        return make_response('Could not verify', 401, {'Authentication': 'Invalid Password."'}) 



@auth.route("/users", methods=["GET"])
class Home(Resource):
    @auth.doc(security='apikey')
    @jwt_required()
    def get(self):
        return [
            {
                'name' : user.name,
                'email' : user.email,
                'password' : user.password
            } for user in UserModel.query.all()
        ]



snf = Namespace('', description='Search and Filter')


@snf.route("/search", methods=["GET"])
class Search(Resource):
    @snf.doc(responses={ 200: 'Success', 401: 'Could not verify' })
    @snf.doc(parser = snf.parser()
            .add_argument('title', type=str, required=False, help='Title')
            .add_argument('minprice', type=str, required=False, help='Min Price')
            .add_argument('maxprice', type=str, required=False, help='Max Price')
            .add_argument('location', type=str, required=True, help='Location')
            .add_argument('amenities', type=str, required=False, help='Ameities')
            .add_argument('sort', type=str, required=False, help='Sort', choices=('asc', 'desc'))
    )
    def get(self):
        data = request.args
        title = data.get('title')
        minprice = data.get('minprice')
        maxprice = data.get('maxprice')
        location = data.get('location')
        amenities = data.get('amenities')
        sort = data.get('sort')
        print(title, minprice, maxprice, location, amenities, sort)
        
        query = {
            "query": {
                "bool": {
                    "must": []
                }
            },
            "sort": [
                # {
                #     "price": {
                #         "order": "asc"
                #     }
                # }
            ]
        }
        query["size"] = 100

        if title:
            if len(title) < 3:
                return make_response('Title should be atleast 3 characters', 400)
            
            title = re.sub(' +', ' ', title.strip()).lower()
            # query["query"]["bool"]["must"].append({"fuzzy": {"title": title}})
            query["query"]["bool"]["must"].append({
                "bool": {
                    "should": [
                        {"fuzzy": {"title": title}}, 
                        {"wildcard": {"title": "*"+title+"*"}}, 
                    ], 
                }}
            )

        if amenities:
            if len(amenities) < 3:
                return make_response('Amenities should be atleast 3 characters', 400)
            
            query["query"]["bool"]["must"].append({"fuzzy": {"amenities": amenities.lower()}})

        if minprice:
            if not minprice.isnumeric() or int(minprice) <= 0:
                return make_response('Invalid minprice', 400)
            query["query"]["bool"]["must"].append({"range": {"price": {"gte": minprice}}})
        
        if maxprice:
            if not maxprice.isnumeric() or int(maxprice) <= 0:
                return make_response('Invalid maxprice', 400)
            query["query"]["bool"]["must"].append({"range": {"price": {"lte": maxprice}}})

        if location:
            location = re.sub(' +', ' ', location.strip()).lower()
            if len(location) < 3:
                return make_response('Location should be atleast 3 characters', 400)
            
            query["query"]["bool"]["must"].append({
                "bool": {
                    "should": [
                        {"fuzzy": {"location": location}}, 
                        {"wildcard": {"location": "*"+location+"*"}}, 
                    ], 
                }}
            )
        
        else:
            return make_response('Location is required', 400)
        
        if sort:
            if sort != 'asc' and sort != 'desc':
                return make_response('Invalid sort value', 400)
            query["sort"][0]["price"]["order"] = sort
            
        print(query)
        
        result = es.search(index="properties", body=query)
        res = [item['_source'] for item in result['hits']['hits']]
        if res.__len__() == 0:
            return make_response('No results found', 400)
        return make_response(res, 200)