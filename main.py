# Third party imports
from pydantic import BaseModel, Field

from ms import app
from ms.functions import get_model_response

model_name = "Prediabetes (Diagnostic)"
version = "v1.0.0"


#Inputo for data validation

class Input(BaseModel): #o BaseModel ai, significa que a classe Input herda da classe BaseModel
    gen_hlth: int = Field(..., gt=-1)
    high_bp: int = Field(..., gt=-1)
    high_chol: int = Field(..., gt=-1)
    bmi: int = Field(..., gt=-1)
    income: int = Field(..., gt=-1)
    diffwalk: int = Field(..., gt=-1)
    age: int = Field(..., gt=-1)
    phys_hlth: int = Field(..., gt=-1)
    education: int = Field(..., gt=-1)
    heart_disease_or_attack: int = Field(..., gt=-1)
    phys_activity: int = Field(..., gt=-1)
    men_hlth: int = Field(..., gt=-1)
    chol_check: int = Field(..., gt=-1)

    class Config:
        schema_extra = {
            'GenHlth': 1,
            'HighBP': 0,
            'HighChol': 1,
            'BMI': 32,
            'Income': 5,
            'DiffWalk': 0,
            'Age': 5,
            'PhysHlth': 0,
            'Education': 6,
            'HeartDiseaseorAttack': 0,
            'PhysActivity': 0,
            'MentHlth': 3,
            'CholCheck': 1
        }


# Output for data validation
class Output(BaseModel):
    label: str
    prediction: int

# API routes

@app.get('/')

async def model_info():
    return {
        "name": model_name,
        "version": version
    }

@app.get('/health')
async def service_health():
    return {
        "ok"
    }

@app.post('/predict', response_model = Output)
async def model_predict(input: Input):
    response = get_model_response(input)
    return response
# para criar um ambiente virtual digite terminal, dentro da pasta "python -m venv env" o env e o nome do ambiente virtual, entao pode ser qualquer coisa
# Para ativar o servidor local precisa estar na pasta da api e digitar no terminal ".\env\Scripts\activate"
# Apos isso, digite "uvicorn main:app --reload" para inicializar a api, se o main.py por exemplo estiver em uma pasta fica "uvicorn pasta.main:app --reload"
# para instalar todos os pacotes do requirements.txt : "pip install -r requirements.txt",
#para ver se esta tudo instalado: "pip freeze"

# o Docker cria um container, contendo a aplicacao e disponivel para ser executada (ele cria uma imagem da api)
# criar um container do docker "docker build . -t prediabetes_classifier_docker"
# excutar docker criado "docker run -p 8000:8000 prediabetes_classifier_docker"

