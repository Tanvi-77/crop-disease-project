1. create project folder


2. created files and folders using commands
mkdir dataset
  mkdir dataset\raw
  mkdir dataset\processed
  mkdir dataset\split
  New-Item dataset\select_dataset.py -ItemType File  

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

then added code in .gitignore and added only required files and folders in git repo so git repo will not become heavy and remain lightweight   (basically controlled what Git tracks)


note : requirements.txt = list of dependencies needed to run your project    (so anyone Medha, teacher, future me 
can install the same environment)
Medha will just run :  pip install -r requirements.txt
and her setup becomes exactly like yours

5. push initial structure into gitHub repo
commit changes
add repo link
create Main branch
push the code into gitHub repo  (initial project setup)


create branches
  git checkout -b ml-dev       // create ml-dev branch and switch to it
  git push origin ml-dev       // push branch  to gitHub
  git checkout main            // back to main banch
  git checkout -b app-dev      // create app-dev branch and switch to it
  git push origin app-dev      // push branch to gitHub


6. download dataset

inside raw folder  
  Tomato_healthy
  Tomato_Early_blight
  Tomato_Late_blight
  potatohHealthy
  potatp_Early_blight
  potato_Late_blight
  pepper_bell_healthy
  pepper_bell_Bacterial_spot


prject exceution:
1. Data preprocessing :
   out of 1000 took only 400
   converts raw imges into numerical array
   images resized and normalise
   Ready for training


2. Model training : MobileNetV2 Transfer Learning  -- pretrained cnn model trained already on millions of imges and we use transfer learning means no model training from scratch , reusing existing learned features for faster and better accuracy
   Load preprocessing data
   Split train/test
   Load MobileNetV2
   Train model
   Save  .h5 model and labels.json  

run either :
  python preprocessing/preprocess.py
  OR 
  python training/train_model.py


  . training data = 2361 imges
  . testing data = 591 imges
  . total images = 2952 imges

  . Accuracy : How correctly model predicts on training data -- accuracy = 0.9754
  . val_accuracy : How correctly model predicts on unseen test/validation data  -- 0.9272
  . loss : How wrongly predicted on testing data -- 0.0855 
  . val loss : How wrongly predicted on training data-- 0.2186


  3. predictor.py : it will :
    ✅ Load trained model
    ✅ Load labels
    ✅ Take image path
    ✅ Predict disease
    ✅ Return confidence score
    ✅ Return solution

  4. test_predictor.py
    This file is for testing purpose where img path is given to predict the class and solution 
     
    

    


    


  