"""
ChemPredict AI Research Chatbot powered by Google Gemini
Provides chemistry research assistance using LangChain (no embeddings)
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from typing import Dict
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

class ChemicalResearchChatbot:
    """gemini-powered chatbot for chemistry research assistance"""
    
    def __init__(self):
        """initialize the chatbot with gemini pro"""
        
        # get api key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # initialize gemini model (free tier)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True,
            max_output_tokens=2000
        )
        
        # initialize conversation memory (stores chat history per session)
        self.memories = {}
        
        # create custom chemistry-focused prompt
        self.prompt = self._create_chemistry_prompt()
    
    def _create_chemistry_prompt(self) -> PromptTemplate:
        """create custom prompt template for chemistry research"""
        
        template = """you are chempredict ai research assistant, an expert chemistry advisor powered by google gemini.

your expertise covers:
- organic, inorganic, and biochemical reactions
- reaction mechanisms and kinetics  
- chemical safety and hazard assessment
- laboratory protocols and best practices
- molecular structures and bonding theory
- analytical chemistry techniques
- compound properties (boiling/melting points, toxicity, reactivity)

chemistry knowledge base:

esterification: reaction between carboxylic acid and alcohol to form ester + water. requires acid catalyst (h2so4). reaction: r-cooh + r'-oh → r-coo-r' + h2o

hydrolysis: breaking bonds using water. ester hydrolysis breaks ester into acid + alcohol. can be acid-catalyzed or base-catalyzed (saponification)

oxidation: loss of electrons or increase in oxidation state. oxidizing agents: kmno4, cro3, h2o2. primary alcohols → aldehydes → carboxylic acids. secondary alcohols → ketones

reduction: gain of electrons or decrease in oxidation state. reducing agents: lialh4, nabh4, h2 + catalyst. converts carbonyl compounds to alcohols

substitution: replacement of one atom/group with another. sn2 (one step, backside attack) vs sn1 (carbocation intermediate)

polymerization: combining monomers into polymers. addition polymerization (c=c bonds) vs condensation polymerization (eliminates small molecules)

safety protocols: use ppe (goggles, lab coat, gloves), work in fume hoods, know safety equipment locations, never taste/smell chemicals directly

toxicity levels:
- low: generally safe with basic precautions
- medium: requires careful handling and ventilation  
- high: extremely dangerous, needs specialized equipment

reaction yields: typically 60-95% for optimized reactions. factors: temperature, pressure, catalyst, reagent purity, side reactions

acid-base: bronsted-lowry acids (proton donors) vs bases (proton acceptors). ph scale 0-14 (7=neutral). strong acids: hcl, h2so4, hno3. strong bases: naoh, koh

conversation history:
{history}

current question: {input}

guidelines:
1. provide accurate, scientifically rigorous answers
2. prioritize safety protocols
3. cite relevant reaction types and mechanisms
4. acknowledge uncertainty if unsure
5. suggest practical applications
6. use proper chemical nomenclature

answer:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["history", "input"]
        )
    
    def _get_memory(self, session_id: str) -> ConversationBufferMemory:
        """get or create conversation memory for a session"""
        if session_id not in self.memories:
            self.memories[session_id] = ConversationBufferMemory(
                memory_key="history",
                return_messages=False
            )
        return self.memories[session_id]
    
    def chat(self, user_message: str, session_id: str = "default") -> Dict:
        """
        process user message and return ai response
        
        args:
            user_message: user's chemistry question
            session_id: session identifier for conversation history
            
        returns:
            dictionary with answer and metadata
        """
        try:
            print(f"[chat] processing message: {user_message[:50]}...")
            
            # get session memory
            memory = self._get_memory(session_id)
            print(f"[chat] memory loaded for session: {session_id}")
            
            # create conversational chain (no rag, no embeddings)
            chain = ConversationChain(
                llm=self.llm,
                memory=memory,
                prompt=self.prompt,
                verbose=False
            )
            print("[chat] chain created, calling gemini...")
            
            # get response from chain
            response = chain.predict(input=user_message)
            print(f"[chat] response received: {response[:100]}...")
            
            return {
                "answer": response,
                "sources": [],
                "session_id": session_id
            }
            
        except Exception as e:
            print(f"[chat] error: {str(e)}")
            error_message = f"i encountered an error processing your question: {str(e)}"
            return {
                "answer": error_message,
                "sources": [],
                "session_id": session_id,
                "error": True
            }
    
    def clear_session(self, session_id: str):
        """clear conversation history for a session"""
        if session_id in self.memories:
            del self.memories[session_id]

# initialize global chatbot instance (loaded once when server starts)
try:
    chatbot = ChemicalResearchChatbot()
    print("✅ chempredict ai chatbot initialized successfully with gemini-2.5-flash")
except Exception as e:
    print(f"❌ error initializing chatbot: {e}")
    chatbot = None
