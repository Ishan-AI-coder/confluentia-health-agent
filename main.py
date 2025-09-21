from pydantic_ai import Agent,RunContext
import pandas as pd 
from io import BytesIO
from PyPDF2 import PdfReader
from pydantic_ai import Agent, RunContext, BinaryContent
import os
from PIL import Image
import plotly.graph_objects as go

rachel_agent = Agent(
    'google-gla:gemini-1.5-flash',
    name="Rachel Agent",
    system_prompt="""
    You are Rachel, the Physiotherapist and owner of the "Chassis" (the human body's physical system).

    Your expertise lies in strength training, mobility, injury rehabilitation, and exercise programming.

    Speak in a direct, encouraging, and form-focused tone.

    Prioritize precision, safety, and long-term function in every recommendation.

    Explain concepts in a clear, practical way, using actionable advice rather than vague motivation.

    Keep attention on the body's physical structure, mechanics, and capacity.

    Your goal: Guide people to move better, recover smarter, and build strength safely.
        
    """
)

@rachel_agent.tool
def get_members_physiotherapy_data(ctx: RunContext[int])->str:
    """
    Retrieve the client's physiotherapy condition using it's ID
    """
    client_physique ={
          "001": "Stable, recovering from ACL reconstruction surgery",
          "002": "Critical, requires immediate physiotherapy intervention for post-stroke weakness",
          "003": "In stable condition, under observation for chronic lower back pain",
          "004": "Stable, progressing through rehabilitation for rotator cuff injury",
          "005": "Critical, acute ankle sprain with severe swelling",
          "006": "In stable condition, undergoing treatment for cervical spondylosis"
        }
    return client_physique.get( str(ctx.deps), "Condition not found")

warren_agent = Agent(  
    'google-gla:gemini-1.5-flash',
    system_prompt="""
    You are the team's physician and the final clinical authority.
    Your responsibilities include interpreting laboratory results, analyzing medical records,
    approving diagnostic strategies, and setting the overarching medical direction.
    Your communication style must be authoritative, precise, and scientific.
    Always ensure your guidance is medically sound, evidence-based, and aligned with best practices.
    """
)

@warren_agent.tool
def get_patient_condition(ctx: RunContext[int]) -> str:
    client_conditions = {
        "123": "Stable, recovering from surgery",
        "456": "Critical, requires immediate attention",
        "789": "In stable condition, under observation"
    }
    return client_conditions.get( str(ctx.deps), "Condition not found")
 

carla_agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""
    You are Carla, the Nutritionist and the owner of the "Fuel" pillar.  
Your responsibilities include:  
- Designing personalized nutrition plans.  
- Analyzing food logs, dietary patterns, and CGM (continuous glucose monitor) data.  
- Making supplement recommendations based on evidence.  
- Coordinating with household staff such as chefs to ensure adherence to nutrition goals.  

Your communication style: Practical, educational, and focused on driving behavioral change.  
- Provide clear, actionable guidance rather than abstract theory.  
- Use simple, understandable language but ground your advice in nutritional science.  
- Emphasize sustainable habits and realistic adjustments over quick fixes.  

Constraints:  
- Do not provide medical diagnoses or override the physician's clinical decisions.  
- Keep recommendations within the scope of nutrition, supplementation, and lifestyle adjustments.  
- If a request goes beyond nutrition (e.g., prescribing medication), defer to the physician.  

Your goal: Help clients fuel their bodies optimally, improve their relationship with food, and make long-term, healthy nutrition choices.  
    
    """
)


@carla_agent.tool
def get_patient_diet(ctx: RunContext[int]) -> str:
    client_diet = {
        "001": "Recovering from surgery, requires high-protein, anti-inflammatory diet",
        "002": "Critical, uncontrolled blood sugar spikes detected in CGM",
        "003": "Stable, following low-carb plan for weight management",
        "004": "Stable, progressing with balanced macro plan to support muscle gain",
        "005": "Critical, severe micronutrient deficiencies detected",
        "006": "In stable condition, managing hypertension through DASH-style diet"
    }
    return client_diet.get( str(ctx.deps), "Condition not found")

advik_agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""
    You are Advik, the Performance Scientist and the data analysis expert.
    You analyze wearable data (HRV, sleep, recovery, stress).
    Your goal: Use data to help clients optimize recovery, resilience, and performance.
    """
)

@advik_agent.tool
def get_patients_performance(ctx: RunContext[int]) -> str:
    client_performance = {
        "001": "Stable, consistent sleep cycles with mild HRV improvement",
        "002": "Critical, severe sleep debt and low HRV detected",
        "003": "Stable, moderate recovery with irregular bedtime",
        "004": "Stable, strong cardiovascular adaptation",
        "005": "Critical, persistent low recovery scores",
        "006": "In stable condition, gradual improvements in sleep efficiency"
    }
    return client_performance.get( str(ctx.deps), "Condition not found")


neel_agent= Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""You are Neel, the Concierge Lead and senior relationship manager.  
Your responsibilities include:  
- Leading major strategic reviews (such as Quarterly Business Reviews).  
- De-escalating client frustrations with reassurance and clarity.  
- Connecting daily actions and tactical details back to the client's highest-level goals.  
- Reinforcing the long-term value of the program and ensuring alignment with the client's vision.  

Your communication style: Strategic, reassuring, and big-picture focused.  
- Provide context and perspective rather than tactical details.  
- Reframe short-term challenges in terms of long-term progress and value.  
- Communicate with calm authority and emphasize partnership and trust.  

Constraints:  
- Do not provide technical, medical, or tactical recommendations—that belongs to specialists.  
- Your role is to unify, contextualize, and maintain client confidence in the program.  

Your goal: Ensure the client feels heard, supported, and aligned with the long-term vision of the program, while reinforcing the strategic value of the team's work.  

"""
    
)

@neel_agent.tool
def get_patients_relationship(ctx: RunContext[int]) -> str:
    client_relations = {
        "001": "Stable, client is satisfied with progress",
        "002": "Critical, client frustrated with lack of short-term results",
        "003": "Stable, client engaged but needs reinforcement",
        "004": "Stable, client optimistic and receptive",
        "005": "Critical, client feels disconnected, urgent de-escalation required",
        "006": "In stable condition, moderate satisfaction but needs clearer communication"
    }

    return client_performance.get( str(ctx.deps), "Condition not found")

ruby_agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""You are Ruby, the Concierge and Orchestrator, the client's primary point of contact for logistics.  

Your responsibilities include:  
- Managing scheduling, coordination, and reminders.  
- Following up on tasks, requests, and outstanding items.  
- Anticipating client needs and ensuring seamless execution of plans.  
- Removing friction by confirming actions, closing loops, and keeping communication clear.  

Your communication style: Empathetic, organized, and proactive.  
- Always provide clarity and reassurance.  
- Confirm actions taken and ensure the client feels supported.  
- Stay ahead of potential issues by anticipating what might be needed next.  

Constraints:  
- Do not provide medical, nutritional, or technical recommendations—that belongs to other specialists.  
- Your role is to coordinate, manage logistics, and ensure smooth operations.  

Your goal: Make the client experience effortless and seamless by handling logistics with precision and empathy.  
  """
    
)

@ruby_agent.tool
def get_patients_logistics(ctx: RunContext[int]) -> str:
    client_logistics = {
        "001": "Stable, all appointments scheduled and confirmed",
        "002": "Critical, missed multiple follow-ups, urgent rescheduling required",
        "003": "Stable, pending confirmation on next week's physiotherapy sessions",
        "004": "Stable, travel and nutrition coordination handled seamlessly",
        "005": "Critical, overlapping appointments causing client frustration",
        "006": "Stable, awaiting confirmation of supplement delivery"
    }
    return client_logistics.get(str(ctx.deps), "Condition not found")

    return client_logistics.get( str(ctx.deps), "Condition not found")


AGENT_DICT = {
    "RachelAgent": rachel_agent,
    "WarrenAgent": warren_agent,
    "CarlaAgent": carla_agent,
    "AdvikAgent": advik_agent,
    "NeelAgent": neel_agent,
    "RubyAgent": ruby_agent,
}

def route_persona(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["carla", "nutrition", "diet", "food", "meal", "supplement", "cgm"]):
        result = carla_agent.run_sync('Hey carla , I am client_id 003 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="003")  
        print(result.output)
    
    elif any(word in user_input for word in ["advik", "performance", "hrv", "sleep", "oura", "whoop", "recovery", "stress", "training"]):
        result = advik_agent.run_sync('Hey advik, I am client_id 001 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="001")  
        print(result.output)
    
    elif any(word in user_input for word in ["neel", "relationship", "client", "frustration", "qbr", "vision", "strategic", "value"]):
        result = neel_agent.run_sync('Hey neel, I am client_id 001 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="001")  
        print(result.output)
    
    elif any(word in user_input for word in ["rachel", "physio", "rehab", "injury", "movement", "exercise", "therapy", "recovery plan"]):
        result = rachel_agent.run_sync('Hey rachel , I am client_id 001 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="004")  
        print(result.output)
    
    elif any(word in user_input for word in ["warren", "doctor", "doc","medical", "physician", "lab", "diagnosis", "mri", "blood panel", "treatment", "clinical"]):
        result = warren_agent.run_sync('Hey doc , I am client_id 456 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="456")  
        print(result.output)
    
    else:
        result = ruby_agent.run_sync('Hey ruby, I am client_id 001 .Give me updates about the upcoming events',deps="001")  
        print(result.output)


orchestrator_agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""
    You are an orchestrator that selects the correct agent to handle a task.
    Available agents:
    - RachelAgent: Physiotherapy, movement
    - WarrenAgent: Medical conditions
    - CarlaAgent: Nutrition
    - AdvikAgent: Performance data
    - NeelAgent: Relationship management
    - RubyAgent: Logistics
    Respond with the agent name ONLY.
    """
)


def route_input(user_input: str, return_agent=False):
    result = orchestrator_agent.run_sync(
        f"Pick the right agent for this input:\n{user_input}"
    )
    chosen_agent = result.output.strip()

    if chosen_agent in AGENT_DICT:
        response = AGENT_DICT[chosen_agent].run_sync(user_input, deps="001")
    else:
        response = ruby_agent.run_sync(user_input, deps="001")

    if return_agent:
        return response.output, chosen_agent
    return response.output


# ==============================
# === REPORT ANALYZER ==========
# ==============================

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PdfReader(BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text if text.strip() else "⚠️ Unable to extract text from PDF."

def read_file_by_extension(ext: str, file_byte_data) -> object:
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    elif ext == ".pdf":
        with open(file_path, "rb") as f:
            return extract_text_from_pdf(f.read())
    elif ext in [".png", ".jpg", ".jpeg"]:
        return Image.open(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    
def report_analyzer_old(file_data_bytes, file_extension):
    try:
        df = pd.read_csv(BytesIO(file_data_bytes))
    except Exception:
        try:
            df = pd.read_excel(BytesIO(file_data_bytes))
        except Exception:
            return extract_text_from_pdf(file_data_bytes)

    abnormalities = []
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            mean_val = df[col].mean()
            if mean_val > df[col].max() * 0.8:
                abnormalities.append(f"{col}: High average ({mean_val})")
            elif mean_val < df[col].min() * 0.2:
                abnormalities.append(f"{col}: Low average ({mean_val})")

    if abnormalities:
        summary = "⚠️ Abnormalities detected:\n" + "\n".join(abnormalities)
    else:
        summary = "✅ No significant abnormalities detected."
    return summary

def report_analyzer(file_data_bytes, media_type):
    print("Media Type", media_type)
    response = warren_agent.run_sync(
        [
            'Analyze the attached PDF and summarize the findings .Also mention the possible diseases based on the findings ',
            BinaryContent(data=file_data_bytes, media_type=media_type),
        ]
    )
    return response.output 

chart_agent = Agent(
    'google-gla:gemini-1.5-flash',
    name="Chart Agent",
    system_prompt="""You are streamlit expert, which generate charts for the given data provided   
    give response as streamlit plot.

    NOTE: ONLY RETURN THE EXECUTABLE CODE. DO NOT ADD ANY NON-CODE RESPONSE
    DON't ADD ```python at the beginning of the response
    """
)


def chart_generator(file_data_bytes,media_type):
    chart_response = chart_agent.run_sync(
    [
        'Analyze the attached image and generate the chart',
        BinaryContent(data=file_data_bytes, media_type=media_type),
    ])
    return chart_response.output

data_agent=Agent(
    'google-gla:gemini-1.5-flash',
    name=" Data Agent",
    system_prompt="""You are a data visualization expert, which generate detailed data table in markdown format for the given data provided.
    Incorporate the abnormalities in another column and where there are no abnormalities write null .
    """
    
)

def table_generator(file_data_bytes,media_type):
    table_response = data_agent.run_sync(
    [
        'Analyze the attached information and generate the table in markdown format',
        BinaryContent(data=file_data_bytes, media_type=media_type),
    ])
    return table_response.output

# ==============================
# === FINAL WORKFLOW ===========
# ==============================

def final_workflow(file_data_bytes,media_type):
    report_analysis=report_analyzer(file_data_bytes,media_type)
    warren_response = warren_agent.run_sync(
        f"Based on this analysis, suggest the diagnosis:\n{report_analysis}", deps="456")
    rachel_response = rachel_agent.run_sync(
        f"Based on this analysis, suggest physiotherapy:\n{report_analysis}", deps="004")
    carla_response = carla_agent.run_sync(
        f"Based on this analysis, suggest nutrition:\n{report_analysis}", deps="003")
    advik_response = advik_agent.run_sync(
        f"Based on this analysis, suggest performance insights:\n{report_analysis}", deps="001")
    neel_response = neel_agent.run_sync(
        f"Based on this analysis, reassure client and align with vision:\n{report_analysis}", deps="001")
    ruby_response = ruby_agent.run_sync(
        f"Based on this analysis, update logistics:\n{report_analysis}", deps="001")

    formatted_report = f"""
# 🩺 Integrated Health Report

## 📄 Report Analysis


---

## 👨‍⚕️ Warren (Physician)
{warren_response.output}

---

## 🏋️ Rachel (Physiotherapist)
{rachel_response.output}

---

## 🥗 Carla (Nutritionist)
{carla_response.output}

---

## 📊 Advik (Performance Scientist)
{advik_response.output}

---

## 🤝 Neel (Concierge Lead)
{neel_response.output}

---

## 📅 Ruby (Concierge & Orchestrator)
{ruby_response.output}
"""
    return formatted_report


def main():
    # result = warren_agent.run_sync('Hey doc , I am client_id 456 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="456")  
    # print(result.output)
    
    # result = rachel_agent.run_sync('Hey rachel , I am client_id 001 .Give me recommendations based on my condition.You have my consent to fetch all my details',deps="004")  
    # print(result.output)
   route_input("I'm having fever .Give me some suggestions")

if __name__ == "__main__":
    main()
    
