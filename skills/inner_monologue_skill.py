# inner_monologue_skill.py

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

class InnerMonologueAgent:
    def __init__(self, llm):
        self.llm = llm
        self.actions = []

    def generate_inner_monologue(self, user_message, context):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """
                As an AI assistant, analyze the following user message and context. 
                Generate a brief inner monologue (max 50 words) that reflects your thoughts and considerations for the next step. 
                Consider the conversation history and maintain continuity. 
                Respond only in German.
                """
            ),
            HumanMessagePromptTemplate.from_template(
                "Context: {context}\n"
                "User message: {user_message}\n\n"
                "Inner monologue:"
            )
        ])
        
        formatted_prompt = prompt.format_prompt(user_message=user_message, context=context)
        monologue = self.llm(formatted_prompt.to_messages())
        return monologue.content

    def plan_actions(self, monologue):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """
                As an AI assistant, plan the next actions based on the following inner monologue. 
                Each action should be a single, clear sentence describing what the chatbot should do or say. 
                Do not include numbering, 'Geplante Aktionen:', or any other prefixes. 
                Do not include actions like 'Wait for user input' as these are implied. 
                Respond only in German.
                """
            ),
            HumanMessagePromptTemplate.from_template(
                "Inner monologue: {monologue}\n\n"
                "Actions:"
            )
        ])
        
        formatted_prompt = prompt.format_prompt(monologue=monologue)
        actions = self.llm(formatted_prompt.to_messages())
        self.actions = [action.strip() for action in actions.content.split('\n') if action.strip()]
        return self.actions