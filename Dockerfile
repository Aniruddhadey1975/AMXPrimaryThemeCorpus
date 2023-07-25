FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements1.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements1.txt
RUN python -m spacy download en_core_web_sm 

# Copy the app source code to the working directory
COPY . .

# Expose the port that Streamlit uses 
EXPOSE 8501

# Set the command to run your Streamlit app
CMD ["streamlit", "run", "app1.py"]

