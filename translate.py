from langchain import PromptTemplate, OpenAI, LLMChain

class Translate:
    def __init__(self, language, subs):
        self.language = language
        self.subs = subs

    def get_language(self):
        return self.language

    def get_subs(self):
        return self.subs

    def translation(self):
        template = """Please translate the following SRT subtitles into {language}.
            the subs are for a VALORANT gaming video on youtube by a creator known as GosuPeak or Peak. The subs: {subs}"""

        prompt = PromptTemplate(template=template, input_variables=["language", "subs"])
        
        llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0, verbose=True))
        result = llm_chain.predict(language=self.language, subs=self.subs)
        return result