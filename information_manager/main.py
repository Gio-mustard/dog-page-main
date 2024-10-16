from groq_use import get_schema

def get(description:str)->dict:
    if (
        description==""
        or
        len(description)<20
        or 
        description==None
        ):
        raise ValueError("description is required and the min lenght is 20 characters")
    
    return get_schema(description=description) # es la description eh!