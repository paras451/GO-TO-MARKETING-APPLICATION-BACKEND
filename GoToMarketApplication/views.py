from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from GoToMarketApplication.serializers import *
from rest_framework import status

import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@api_view(["POST"])
def generate_marketing_plan(request):
    data = request.data

    final_prompt = f"""
You are a senior go-to-market and digital marketing strategist.

IMPORTANT:
You MUST start your response by REPEATING the provided business details
exactly in a clearly formatted section before giving any strategy.

Do not use emojis.

===== BUSINESS OVERVIEW ====

• Business Name: {data.get('category')}
• Business Type: {data.get('subCategory')}
• Category: {data.get('category')}
• Sub-Category / Niche: {data.get('subCategory')}
• Target Audience: {data.get('targetAudience')}
• Location / Market: {data.get('location')}

==== ONLINE PRESENCE ====

• Website Available: {data.get('hasWebsite')}
• Website URL/Name: {data.get('websiteUrl') if data.get('hasWebsite') == 'yes' else 'Not available'}

• Mobile App Available: {data.get('hasApp')}
• App Name: {data.get('appName') if data.get('hasApp') == 'yes' else 'Not available'}

==== BUSINESS STRATEGY ====

• Primary Goal: {data.get('businessGoal')}
• Trademark Registered: {data.get('trademark')}
• Idea Status: {data.get('ideaStatus')}
• Patent Available: {data.get('hasPatent')}

Create a **complete, actionable Go-To-Market and Digital Marketing Plan**.

The plan MUST include clearly separated sections with headings and bullet points:

### 1️⃣ Go-To-Market Strategy
• Market positioning  
• Unique value proposition  
• Launch & growth approach  

### 2️⃣ SEO Strategy
**On-Page SEO**
• Keyword strategy  
• Website optimization  

**Off-Page SEO**
• Backlinks  
• Authority building  

### 3️⃣ Content Strategy
• Blog ideas  
• Social media content  
• Video & reels ideas  

### 4️⃣ Paid Advertising (PPC)
• Google Ads strategy  
• Social media ads  
• Budget allocation logic  

### 5️⃣ Recommended Tools
• SEO tools  
• Content & editing tools  
• Analytics tools  

### 6️⃣ Website / App Recommendations
• If website/app is missing, suggest what to build  
• UX & conversion tips  

### 7️⃣ 3–6 Month Growth Roadmap
• Month-wise plan  
• Key KPIs to track  

### Suggest Target Audience Segments
• Based on business type and location
• Demographics, interests, behaviors


==== FINAL SUMMARY TABLE (IMPORTANT) ====


At the END, provide a **clear summary table** with the following columns:

| Aspect | Details |
|------|--------|
| Business Type | |
| Target Audience | |
| Primary Goal | |
| Key Marketing Channels | |
| SEO Focus | |
| Paid Ads Focus | |
| Content Focus | |
| Recommended Tools | |
| Expected Outcome (3–6 Months) | |

========================
  FORMAT RULES
========================
• Do Not Merge Sections
• Use clear headings
• Use bullet points
• Keep language simple & professional
• Do NOT write long paragraphs
• Make it easy to read in a web UI
• Space between sections
• Use markdown formatting
  Each detail MUST be on a separate new line.
  DO NOT combine multiple points in a single line.
"""

    try:
        response = client.responses.create(
        model="gpt-5-mini",   
        input=final_prompt
        )
        output_text = response.output_text

        if output_text:
            return Response({"plan": output_text})
        else:
            return Response({"plan": output_text})

    except Exception as e:
        error_message = str(e)
        print("DEBUG ERROR:", error_message)

    # Quota / rate limit error
    if "429" in error_message or "quota" in error_message.lower():
        return Response(
            {
                "error": "Too many requests 🚦 Please try again after some time."
            },
            status=429
        )

    # Timeout or network issue
    if "timeout" in error_message.lower():
        return Response(
            {
                "error": "AI service is slow right now. Please try again."
            },
            status=504
        )

    # Generic fallback (safe for production)
    return Response(
        {
            "error": "Something went wrong on our side. Please try later."
        },
        status=500
    )
    # except Exception as e:
    #     print(f"DEBUG ERROR: {str(e)}")
    #     return Response({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    try:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {"Message": "User registered successfully "},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error default": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
