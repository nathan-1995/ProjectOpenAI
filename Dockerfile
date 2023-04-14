FROM python:slim-buster

# Set the working directory
WORKDIR /app

# Copy the app files and requirements
COPY app.py .
COPY templates templates/
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the OpenAI API key
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
