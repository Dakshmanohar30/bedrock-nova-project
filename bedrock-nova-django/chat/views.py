from rest_framework.decorators import api_view
from rest_framework.response import Response
from .bedrock_client import bedrock_client
from .prompts import (
    SYSTEM_PROMPT,
    INSTRUCTION_PROMPT,
    FEW_SHOT_PROMPT,
    SAFETY_PROMPT,
    TONE_PROMPT,
)

NON_MEDICAL_RESPONSE = "This is not a medical query. I can only assist with clinical or healthcare-related questions."

OUTPUT_FORMAT_PROMPT = """
Respond ONLY in this structure:

1. Patient Summary
2. Key Symptoms
3. Relevant History (if available)
4. Clinical Considerations (non-diagnostic)
5. Possible Differential Categories
6. Recommended Next Evaluation Steps
7. Red Flag Symptoms
8. Safety Disclaimer

End with:
This information is for clinical support only and must be validated by a licensed medical professional.
"""

MEDICAL_TERMS = [
    "pain", "fever", "blood", "pressure", "diabetes", "cough",
    "headache", "dizziness", "nausea", "vomiting", "patient",
    "symptom", "history", "chest", "breath", "infection", "heart"
]

GREETINGS = ["hi", "hello", "hey", "good morning", "good evening"]


@api_view(["POST"])
def chat_with_nova(request):
    user_message = request.data.get("message", "").strip().lower()

    if not user_message:
        return Response({"error": "Message is required"}, status=400)

    # Greeting handler
    if any(greet in user_message for greet in GREETINGS):
        return Response({
            "reply": "Hello! I'm your Doctor Assistant. Please share your clinical question or patient details."
        })

    # Hard non-medical filter
    if not any(term in user_message for term in MEDICAL_TERMS):
        return Response({"reply": NON_MEDICAL_RESPONSE})

    final_prompt = f"""
{SYSTEM_PROMPT}
{INSTRUCTION_PROMPT}
{FEW_SHOT_PROMPT}
{SAFETY_PROMPT}
{TONE_PROMPT}

PATIENT CASE:
{user_message}

{OUTPUT_FORMAT_PROMPT}
"""

    try:
        response = bedrock_client.converse(
            modelId="amazon.nova-pro-v1:0",
            messages=[
                {
                    "role": "user",
                    "content": [{"text": final_prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.2,
                "topP": 0.9,
            }
        )

        reply = response["output"]["message"]["content"][0]["text"]

        # CLEAN MODEL OUTPUT
        reply = reply.replace("**", "")

        reply = reply.replace("Patient Summary", "\nPatient Summary")
        reply = reply.replace("Key Symptoms", "\nKey Symptoms")
        reply = reply.replace("Relevant History", "\nRelevant History")
        reply = reply.replace("Clinical Considerations", "\nClinical Considerations")
        reply = reply.replace("Possible Differential", "\nPossible Differential")
        reply = reply.replace("Recommended Next", "\nRecommended Next")
        reply = reply.replace("Red Flag", "\nRed Flag")
        reply = reply.replace("Safety Disclaimer", "\nSafety Disclaimer")

        reply = "\n".join([line.strip() for line in reply.splitlines() if line.strip()])

        return Response({"reply": reply})

    except Exception:
        return Response({"reply": "Backend not responding."})
