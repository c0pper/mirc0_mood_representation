echo on 
call .\my_env\Scripts\activate.bat
pip install -r requirements.txt
call streamlit run annotations_visual.py