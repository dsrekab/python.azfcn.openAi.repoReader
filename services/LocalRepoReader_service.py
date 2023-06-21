from langchain import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain import PromptTemplate
from langchain.callbacks import get_openai_callback
import os
import logging

class LocalRepoReader:
    def queryForPrompt(self, rootFolder, prompt):
        template = """
        %INSTRUCTIONS:
        I am going to load several code files that I need help understanding.
        Please respond with detailed and technical responses meant for software developers.

        %TEXT:
        {text}
        """
        # Create a LangChain prompt template that we can insert values to later
        prompt = PromptTemplate(
            input_variables=["text"],
            template=template,
        )

        final_prompt = prompt.format(text=prompt)

        loader = DirectoryLoader(rootFolder, glob="**/*.cs", recursive=True)
        documents = loader.load()
                
        ignore_dirs = ['\\bin\\', '\\obj\\']
        filteredCodeFiles = [file for file in documents if not any(ignore_dir in file.metadata['source'] for ignore_dir in ignore_dirs)]
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        text = text_splitter.split_documents(filteredCodeFiles)

        embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
        docsearch = FAISS.from_documents(text,embeddings)
        llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
        
        cbInfo=""
        with get_openai_callback() as cb:
            qa = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=docsearch.as_retriever(),
                                    return_source_documents=True)

            result=qa({"query":final_prompt})
            cbInfo=cb

        doc_names = [docs.metadata['source'] for docs in result['source_documents']]
        doc_name_display = '\n'.join(list(set(doc_names)))

        return f"{result['result']}\n\n---\n{doc_name_display}\n---\n---{cbInfo}---\n"