from fastapi.middleware.cors import CORSMiddleware


# MIDDELEWARE
def add_cors(app):
    app.add_middleware(     #REQUEST/RESPONSE  MIDDLE LA  INTERCEPT PANNURA LAYER ADD PANRA
        CORSMiddleware,
        allow_origins = ["http://localhost:4200", ],  # ONLY THIS ORIGIN ALLOWD/ANGULAR APP ONLY ALLOWED
        allow_credentials = True ,    # COOKIES / AUTH TOKEN ALLOWED  (LOGIN SYSTEM JWT / SESSION)
        allow_methods = ["*"] ,  # GET ,POST , PUT , DELETE  ->ALL ARE ALLOW
        allow_headers = ["Authorization" , "Content-Type"] ,   # CUSTOM HEADER ALLOOW  EXAMPLE : 1) AUTHORIZATION TOKEN 2) CONTENT-TYPE
)