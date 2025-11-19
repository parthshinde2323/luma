
import google.generativeai as genai
import random
import re
import json

class Autism:
    def __init__(self):
        # to set up my gemini api key
        genai.configure(api_key="AIzaSyDvxslGJj1vvfZtQm2QLH75xzRurZ3R9gg")

        self.model = genai.GenerativeModel("gemini-2.0-flash")
        # self.model = genai.GenerativeModel(
        #     "gemini-2.0-flash",
        #     generation_config={
        #         "temperature": 1.0,          # HIGHER randomness
        #         "top_p": 0.95,
        #         "top_k": 40,
        #         "max_output_tokens": 100
        #     }
        # )

        # list of tones the sentence can be of and to select from
        self.tones = ["happy", "neutral", "sarcastic", "angry"]   

    
    # function with prompt to generate sentence with the correct option as answer in json format
    def generate_question(self):
        seed = random.randint(1, 999999)
        prompt = f"""
        You are generating a unique sentence each time.
        Seed: {seed}
        
        Generate ONE short natural sentence that has a clear emotional tone.

        Determine its tone from one of the following:
        {", ".join(self.tones)}

        Respond ONLY in raw JSON (NO code block, NO explanation):
        {{
            "sentence": "....",
            "tone": "{'|'.join(self.tones)}"
        }}
        """

        response = self.model.generate_content(prompt)
        raw = response.text.strip()

        try:
            result = json.loads(raw)
        except:
            # use regular expression to extract the json
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not match:
                raise ValueError(f"Model did not return JSON. Response was:\n{raw}")
            json_text = match.group(0)
            result = json.loads(json_text)

        correct = result["tone"]

        wrong = [t for t in self.tones if t != correct]
        random.shuffle(wrong)

        options = [correct] + wrong[:3]

        return {
            "sentence": result["sentence"],
            "correct": correct,
            "options": options
        }

    
    def check_answer(self, user_answer, correct_answer):
        return user_answer.lower() == correct_answer.lower()
