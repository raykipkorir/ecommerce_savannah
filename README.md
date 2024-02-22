# Ecommerce Savannah
#### Backend Technical challenge
### Available functionalities
1. Users can sign in via Google or GitHub. Once signed in a cart instance is created.
2. Users can add products to cart as well as increment or decrement the quantity of the product in cart.
3. Once the product is added to cart, users can make an order. An SMS will be sent to the phone number provided by the user acknowledging the order made.
4. Staff and admin can update the status of the user's order.
   
## Tech stack
- Django
- PostgreSQL
- Render
- Amazon S3
- Docker and docker-compose
- GitHub Actions
- Africa's talking

## API documentation
- [Swagger documentation](https://ecommerce-savannah.onrender.com/api/schema/swagger/)

- [Redoc documentation](https://ecommerce-savannah.onrender.com/api/schema/redoc/)

- [Postman collection](https://www.postman.com/raykipkorir/workspace/public-workspace/request/19883034-99678c5d-b4dd-4fc9-9651-1bb48fc68bb6)
## Authentication
Users can sign up and login using Google or Github
- [Google Auth url](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://ecommerce-savannah.onrender.com/api/google-callback/&prompt=consent&response_type=code&client_id=611241998884-3vt81edvfbvca97515qrqpha6rghfcqt.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline)
- [Github Auth url](https://github.com/login/oauth/authorize?client_id=b3613d55c08b9555021f&redirect_uri=https://ecommerce-savannah.onrender.com/api/github-callback/&scope=user)

## Tests
Backend test coverage - 95%

## CI/CD
Integrated Github Actions

## Deployment
Deployed on Render -> [Ecommerce Savannah](https://ecommerce-savannah.onrender.com)
