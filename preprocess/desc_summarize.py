import re
import json
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain


class SummarizeDesc:
    """
    summarize descriptions from feature list JSON
    """

    @staticmethod
    def feature_summary_dict(features_data, model, outfile_name) -> dict:
        template = """
        You are an helpful assistant trying to answer user question in a 
        conversational manner.

        Follow the instructions below to accomplish the task:
        - Please summarize the following text in less than 100 characters.
        - Start your answer with "This feature describes".
        - Please provide the output in a manner that <requirements> would understand.
        - The document you have to summarize is delimited by the 
            <document> </document> tags.
        - Output the answer inside <answer> </answer> tags.
        """

        prompt = ChatPromptTemplate.from_messages(
            [("system", template), ("human", "<document>{text}</document>")]
        )

        chain = load_summarize_chain(model, chain_type="stuff", prompt=prompt)

        summaryDict = {}
        # keep track of missed keys, if any
        missed_keys = []

        for key in features_data.keys():
            desc = features_data.get(key)
            docs = [Document(page_content=desc)]

            try:
                output = chain.invoke(docs)

                # edit a way to parse xml tags
                summary_output = output["output_text"]
                summaryDict[key] = outfile_summary

                # add to json file as soon as one key is processed
                with open(
                    outfile_name,
                    "w",
                ) as outfile:
                    json.dump(summaryDict, outfile, indent=4)

            except:
                missed_keys.append(key)
                time.sleep(62)

        # need to find a way to run the missed keys list