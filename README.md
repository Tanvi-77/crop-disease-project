1. create project folder


2. created files and folders using commands
mkdir dataset
  mkdir dataset\raw
  mkdir dataset\processed
  mkdir dataset\split

mkdir preprocessing
  New-Item preprocessing\preprocess.py -ItemType File

mkdir training
  New-Item training\train_model.py -ItemType File
  New-Item training\evaluate_model.py -ItemType File
  New-Item training\config.py -ItemType File

mkdir model
  New-Item model\labels.json -ItemType File

mkdir utils
  New-Item utils\predictor.py -ItemType File
  New-Item utils\solution_mapper.py -ItemType File

mkdir app
  New-Item app\app.py -ItemType File
  mkdir app\pages  -- folder
  mkdir app\components

mkdir database
  New-Item database\db.py -ItemType File
  New-Item database\history.db -ItemType File

mkdir uploads
mkdir outputs


3. setup
python -m venv venv  --  venv(envrinment name)
venv\Scripts\activate   -- activate env
python -m pip install tensorflow opencv-python numpy pandas matplotlib scikit-learn streamlit pillow  -- installing libraries


note : requirements.txt = list of dependencies needed to run your project    (so anyone Medha, teacher, future me 
can install the same environment)
Medha will just run :  pip install -r requirements.txt
and her setup becomes exactly like yours


