from pydantic import BaseModel, Field, EmailStr
from typing import List

#classe x signup
class UserSchema(BaseModel):
    fullname: str = Field(...)
    born_date: str = Field(...)
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    privacy_account: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "fullname": "Andrea Rossi",
                "born_date": "2022-12-27",
                "email": "mail@mail.com",
                "username": "andrea",
                "password": "ciao",
                "privacy_account": 0,
            }
        }



#classe mandata al server per cambiare le mie informazioni
class UpdateMyInfo(BaseModel):
    token: str = Field(...)
    fullname: str = Field(...)
    born_date: str = Field(...)
    description: str = Field(...)
    privacy_account: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Andrea Rossi",
                "born_date": "2022-12-27",
                "description": "nuova descrizione",
                "privacy_account": 0
            }
        }
#classe x il login o quando chiedo il cambio password
class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "andrea",
                "password": "ciao"
            }
        }

#classe per quando richiedo il mio profilo
class TokenLoginSchema(BaseModel):
    token: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWJkdWxhemVlekB4LmNvbSIsImV4cGlyZXMiOjE2ODI1MTAzMzcuMDk5NzMyMn0.ciwKn1VHjwVdDTw574q9CKVTCZsyEvtQrf55lSb0Z9E"
            }
        }

        
class ChangePublicFlag(BaseModel):
    token: str = Field(...)
    id_post: str
    action: bool



class DeletePost(BaseModel):
    token: str = Field(...)
    id_post: str

class NewTicketSchema(BaseModel):
    token: str 
    subject: str
    content: str
    category: int


class messageOBJ(BaseModel):
    id_user_sender: str
    id_user_recipient: str
    creation_date: str
    content: str
    id_chat: str
    
class NewChatOBJ(BaseModel):
    token: str
    username: str
    

#classe x cambio pw
class NewPWSchema(BaseModel):
    token: str = Field(...)
    current: str = Field(...)
    new: str = Field(...)

class resetPWSchema(BaseModel):
    token: str = Field(...)
    new: str = Field(...)

class emailSchema(BaseModel):
    email: str


class deleteAccountSchema(BaseModel):
    token: str
    pw: str


#classe x cambio username
class NewUsernameSchema(BaseModel):
    token: str = Field(...)
    new: str = Field(...)

class EditPostSchema(BaseModel):
    token: str = Field(...)
    id_post: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    comment_flag: bool = Field(...)
    public_flag: bool = Field(...) 

#Classe x la creazione di un nuovo post
class PostSchema(BaseModel):
    token: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    comment_flag: bool = Field(...)
    public_flag: bool = Field(...)
    
#Questa classe viene restituita x la sezione "info" quando visualizzo il mio profilo
class UserTableSchema(BaseModel):
    id_user: str = Field(...)
    username: str = None
    state: int = Field(...)
    fullname: str = Field(...)
    born_date: str = Field(...)
    profile_pic: str = None
    description: str = None
    privacy_account: bool = Field(...)
    registration_date: str = Field(...)
    number_of_followers: int = 0
    number_of_posts: int = 0
    number_of_like: int = 0


#Questa classe viene restituita x ogni singolo post quando sono nella sezione "posts" del mio profilo 
class myPost(BaseModel):
    id_post: str = Field(...)
    id_user: str = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    creation_date: str = Field(...)
    comment_flag: bool = Field(...)
    public_flag: bool = Field(...)

#Classe per il cambio o la rimozione dell'immagine
class PicUrlSchema(BaseModel):
    token: str = Field(...)
    url: str = Field(...)

class CommentSchema(BaseModel):
    id_comment: str = Field(...)
    username: str = Field(...)
    content: str = Field(...)
    creation_date: str =  Field(...)
    profile_pic: str = None
    is_there_like: bool = False
    number_of_like: int = 0
    reference_comment: str = None

class GetPostSchema(BaseModel):
    id_post: str = Field(...)
    fullname: str = Field(...)
    username: str = Field(...)
    profile_pic: str = None
    title: str = Field(...)
    content: str = Field(...)
    creation_date: str = Field(...)
    comment_flag: bool = Field(...)
    number_of_like: bool = False
    is_there_like: bool = False
    number_of_like: int = 0
    comments: List[CommentSchema] = []


class UpdateRelation(BaseModel):
    token: str = Field(...)
    new_state: int = Field(...)
    username_recipient: str = Field(...)

class relationSchema(BaseModel):
    state_request: int = Field(...)
    id_follow: str = Field(...)
    id_user_sender: str = Field(...)
    date_creation: str = Field(...)
    username: str = Field(...)
    fullname: str = Field(...)
    profile_pic: str = None

class RelationAnswer(BaseModel):
    token: str = Field(...)
    answer: bool = Field(...)
    id_follow: str = Field(...)

class newCommentSchema(BaseModel):
    token: str = Field(...)
    id_post: str = Field(...)
    content: str = Field(...)
    reference_comment: str = None

class likeSchema(BaseModel):
    token: str = Field(...)
    id_element: str = Field(...)
    like: bool = Field(...)

class searchUser(BaseModel):
    fullname: str = Field(...)
    username: str = Field(...)
    profile_pic: str = None