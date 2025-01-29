import sys
import warnings


from crew import ProductAreaGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
from dotenv import load_dotenv

load_dotenv()

ProductAreaGenerator().crew().kickoff()
input = ""