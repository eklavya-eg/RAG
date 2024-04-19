# Retrieval Augmented Generation

This repository contains a retrieval augmented generation system implemented in Python version 11.4.0. The system utilizes Langchain and Chainlit libraries.

## Components

- **Chainlit**: The system uses Chainlit for running the main application. To run Chainlit on port 8002, execute the following command:

- **Model (LLAMA2)**: The system employs the LLAMA2 model for chatting. You can find the model [here](https://huggingface.co/TheBloke/Llama-2-7B-GGML/blob/main/llama-2-7b.ggmlv3.q8_0.bin).

- **Typsense**: Typsense is utilized for retrieval and searching through documents. It runs on port 8081 with self-hosting using Docker. To install Typesense for local hosting, execute: (docker pull typesense/typesense

)
To run with API key "xyz", execute: (docker run -p 8108:8108 -v %cd%/typesense-data:/data typesense/typesense:26.0 --data-dir /data --api-key="xyz" --enable-cors)

- **Universal Sentence Encoder Model**: Google's Universal Sentence Encoder model is used for sentence embeddings. You can access the model [here](https://www.kaggle.com/models/google/universal-sentence-encoder).

## Output Video
Check out the output video [here](https://drive.google.com/file/d/1jYg7tcU5qCWbTGGUIPsLYLXOxMnIQ2Wm/view?usp=sharing).

## Running the System
1. Download the necessary models and Typsense.
2. Set up the paths to the models in `main.py`.
3. Run Typsense for self-hosting.
4. Run Chainlit command to use the application:

Feel free to contribute, report issues, or provide feedback!
