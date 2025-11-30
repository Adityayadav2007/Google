import json
from google import genai

class BaseAgent:
    def __init__(self, name, api_key, model="gemini-2.5-flash"):
        self.name = name
        self.model = model
        self.mem_file = f"memory_{name}.json"
        self.client = genai.Client(api_key=api_key)

        try:
            open(self.mem_file, "x").write(json.dumps([]))
        except:
            pass

    def load_memory(self):
        with open(self.mem_file, "r") as f:
            return json.load(f)

    def save_memory(self, message):
        mem = self.load_memory()
        mem.append(message)
        with open(self.mem_file, "w") as f:
            json.dump(mem, f, indent=2)

    def retrieve(self, query):
        import glob
        text = ""
        for file in glob.glob("docs/*.txt"):
            text += open(file).read() + "\n"
        return text[:4000]

    def think(self, user_input):
        rag = self.retrieve(user_input)

        prompt = f"""
You are {self.name}. You can THINK and use memory and documents.

CONTEXT:
{rag}

User: {user_input}

Respond with a clear, detailed solution.
"""

        result = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        ).text

        return result

    def run(self, user_input):
        response = self.think(user_input)
        self.save_memory({"user": user_input, "answer": response})
        return response
