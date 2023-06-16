# python.azfcn.openAi.repoReader
Read code repository and allow it to be queried by openAI

To get started, after cloning, the following installs will need to be run:
```
python.exe -m pip install --upgrade pip
pip install langchain
pip install openAi
pip install tiktoken
pip install faiss-cpu
pip install unstructured
```

You will also need to adjust settings to your local.settings.json
```
"AzureWebJobsStorage": "UseDevelopmentStorage=true",
"OPENAI_API_KEY":"[your_api_key]"
```