# Python version
FROM python3.10.12

# Workdir
WORKDIR /home/ubuntu/API_DAM_gestionUsuarios

# Set virtual env
RUN python3 -m venv venv 

# Run venv and Install requeriments if it is required
RUN  source venv/bin/activate
RUN  pip install --no-cache-dir --upgrade -r requirements.txt


# ?ENV variables
WORKDIR /home/ubuntu/API_DAM_gestionUsuarios

# Run the API
CMD [ "python3", "main.py"]
