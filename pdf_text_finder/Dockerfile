FROM streamlit/base-deps:1.3.0

# Install libpoppler-cpp-dev
RUN apt-get update && apt-get install -y libpoppler-cpp-dev

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app files
COPY *.py /app/

# Expose the Streamlit port
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "/app/app.py"]
