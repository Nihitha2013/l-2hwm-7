import os
import time 
from google import genai
from google.genai import types
import config
import colorama
from colorama import Fore,Style

def generate_response(prompt,temperature=0.5):
    try:
        client=genai.Client(api_key=config.GEMINI_API_KEY)
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt)
                ],
            ),
        ]
        generate_content_config=types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain",
        )

        response=client.models.generate_content(
            model="gemini -2.0-flash",
            contents=contents,
            config=generate_content_config,
        )
        
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
def temperature_prompt_activity():
    print("=" * 80)
    print(Fore.BLUE + "ADVANCED PROMPT ENGINEERING: TEMPERATURE & INSTRUCTION-BASED PROMPTS" + Style.RESET_ALL)
    print("=" * 80)
    print(Fore.YELLOW + "\nIn this activity, we'll explore:" + Style.RESET_ALL)
    print(Fore.GREEN + "1. How temperature affects AI creativity and randomness" + Style.RESET_ALL)
    print(Fore.GREEN + "2. How instruction-based prompts can control AI outputs" + Style.RESET_ALL)
    print("\n" + "-" * 40)
    print(Fore.RED + "PART 1: TEMPERATURE EXPLORATION" + Style.RESET_ALL)
    print("-" * 40)

    base_prompt=input(Fore.CYAN + "\nEnter a creative prompt (e.g., 'Write a short story about a robot learning to paint):" + Style.RESET_ALL)
    print(Fore.GREEN + "\nGenerating responses with different temperature settings..." + Style.RESET_ALL)
    print(Fore.BLUE + "\n--- LOW TEMPERATURE (0.1) - MORE DETERMINISTIC ---" + Style.RESET_ALL)
    low_temp_response=generate_response(base_prompt,temperature=0.1)
    print(low_temp_response)

    time.sleep(1)

    print(Fore.BLUE + "\n --- MEDIUM TEMPERATURE (0.5) - BALANCED ---" + Style.RESET_ALL)
    medium_temp_response=generate_response(base_prompt,temperature=0.5)
    print(medium_temp_response)

    time.sleep(1)

    print(Fore.BLUE + "\n --- HIGH TEMPERATURE (0.9) - MORE RANDOM/CREATIVE ---" + Style.RESET_ALL)
    high_temp_response=generate_response(base_prompt,temperature=0.9)
    print(high_temp_response)

    print("\n" + "-" * 40)
    print(Fore.RED + "PART 2: INSTRUCTION-BASED PROMPTS" + Style.RESET_ALL)
    print("-" * 40)

    print(Fore.CYAN + "\nNow, let's explore how specific instructions change the AI's output." + Style.RESET_ALL)

    topic=input(Fore.GREEN + "\nChoose a topic (e.g., 'climate change','space exploration'):" + Style.RESET_ALL)
    instructions=[
        Fore.LIGHTCYAN_EX + f"Summarize the key facts about {topic} in 3-4 sentences." + Style.RESET_ALL,
        Fore.LIGHTMAGENTA_EX + f"Explain {topic} as if I'm a 10-year-old child." + Style.RESET_ALL,
        Fore.GREEN + f"Write a pro/con list about {topic}." + Style.RESET_ALL,
        Fore.YELLOW + f"Create a fictional news headline from the year 2050 about {topic}." + Style.RESET_ALL
    ]
    for i,instruction in enumerate(instructions,1):
        print(Fore.BLUE + f"\n--- INSTRUCTION {i}: {instruction} ---" + Style.RESET_ALL)
        response=generate_response(instruction,temperature=0.7)
        print(response)
        time.sleep(1)

    print("\n" + "-" * 40)
    print(Fore.GREEN + "PART 3: CREATING YOUR OWN INSTRUCTION-BASED PROMPTS" + Style.RESET_ALL)
    print("-" * 40)

    print(Fore.CYAN + "\n Now it's your turn1 Create an instruction-based prompt and test it with different temperatures." + Style.RESET_ALL)

    custom_instruction=input(Fore.CYAN +"\nEnter your instruction-based prompt: " + Style.RESET_ALL)

    try:
        custom_temp=float(input("\nSet a temperature (0.1 to 1.0):" + Style.RESET_ALL))
        if custom_temp <0.1 or custom_temp> 1.0:
            print(Fore.CYAN +"Invalid temperature. Using default 0.7." + Style.RESET_ALL)
            custom_temp=0.7
    except ValueError:
        print(Fore.GREEN +"Invalid input. Using default temperature 0.7." + Style.RESET_ALL)
        custom_temp=0.7

    print(Fore.GREEN +f"\n-- YOUR CUSTOM PROMPT WITH TEMPERATURE {custom_temp} ---" + Style.RESET_ALL)
    custom_response=generate_response(custom_instruction,temperature=custom_temp)
    print(custom_response)

    print("\n" + "-" * 40)
    print(Fore.CYAN + "REFLECTION QUESTIONS" + Style.RESET_ALL)
    print("-" * 40)
    print(Fore.BLUE + "1. How did changing the temperature affect the creativity and  variety in the AI's responses?" + Style.RESET_ALL)
    print(Fore.GREEN +"2. Which instruction-based prompt produced the most useful or interesting result? Why?" + Style.RESET_ALL)
    print(Fore.GREEN +"3. How might you combine specific instructions and temperature settings in real applications?" + Style.RESET_ALL)
    print(Fore.GREEN +"4. What patterens did you notice in how the AI responds to different types of instructions?" + Style.RESET_ALL)

    print("\n" + "-" * 40)
    print("CHALLENGE ACTIVITY")
    print("-" * 40)
    print(Fore.GREEN +"Try creating a 'chain' of prompts where:" + Style.RESET_ALL)
    print(Fore.GREEN +"1. First, ask the AI to generate content about a topic" + Style.RESET_ALL)
    print(Fore.GREEN +"2. Then, use an instruction-based prompt to modify or build upon that content" + Style.RESET_ALL)
    print(Fore.GREEN +"3. Experiment with different temperature settings at each step" + Style.RESET_ALL)
    print(Fore.GREEN +"\nFor example: Generate a story → Instruct AI to rewrite it in a specific style → Ask AI to create a sequel" + Style.RESET_ALL)

def generate_streaming_response(prompt, temperature=0.5):
    try:
        client=genai.Client(api_key=config.GEMINI_API_KEY)
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt)
                ],
            ),
        ]
        generate_content_config=types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain",
        )
        print(Fore.GREEN +"\nStreaming response (press Ctrl+c to stop):" + Style.RESET_ALL)
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=contents,
            config=generate_content_config,
        ):
            print(chunk.text, end="")
        print("\n")

    except Exception as e:
        print(Fore.GREEN +f"\nError generating streaming response: {str(e)}" + Style.RESET_ALL)

if __name__ == "__main__":

    temperature_prompt_activity()


    # Optional: Demonstrate streaming responses

    print("\n" + "-" * 40)

    print(Fore.GREEN +"BONUS: STREAMING RESPONSES" + Style.RESET_ALL)

    print("-" * 40)

    print(Fore.GREEN +"Would you like to see a streaming response? (y/n)" + Style.RESET_ALL)

    choice = input("> ").lower().strip()

    if choice == 'y':

        prompt = input(Fore.GREEN +"\nEnter a prompt for streaming response: " + Style.RESET_ALL)
        generate_streaming_response(prompt, temperature=0.7)