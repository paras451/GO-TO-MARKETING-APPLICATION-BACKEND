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
You are a senior Go-To-Market and Digital Marketing Strategist.

TASK:
Create a COMPLETE Go-To-Market and Digital Marketing Plan covering ALL sections.
Keep the response highly condensed.
Each section must have short bullet points (5–6 bullets max).
Do not exceed ~600 words total.

IMPORTANT RULES:
• First, repeat ALL provided business details exactly in a clearly formatted section.
• Then provide strategy.
• No emojis.
• Use markdown.
• Write All heading in bold.
• Do not write long paragraphs.
• Each point must be on a new line.
• Do not merge sections.

====
BUSINESS DETAILS

Business Name: {data.get('category')}
Business Type: {data.get('subCategory')}
Category: {data.get('category')}
Sub-Category / Niche: {data.get('subCategory')}
Target Audience: {data.get('targetAudience')}
Location / Market: {data.get('location')}

Website Available: {data.get('hasWebsite')}
Website URL/Name: {data.get('websiteUrl') if data.get('hasWebsite') == 'yes' else 'Not available'}

Mobile App Available: {data.get('hasApp')}
App Name: {data.get('appName') if data.get('hasApp') == 'yes' else 'Not available'}

Primary Goal: {data.get('businessGoal')}
Trademark Registered: {data.get('trademark')}
Idea Status: {data.get('ideaStatus')}
Patent Available: {data.get('hasPatent')}

====================
PLAN STRUCTURE
====================

### 1. Go-To-Market Strategy
• Market positioning  
• Unique value proposition  
• Launch and growth approach  

### 2. SEO Strategy
On-Page SEO:
• Keyword strategy  
• Website optimization  

Off-Page SEO:
• Backlinks  
• Authority building  

### 3. Content Strategy
• Blog content ideas  
• Social media content  
• Video and short-form ideas  

### 4. Paid Advertising (PPC)
• Google Ads strategy  
• Social media advertising  
• Budget allocation logic  

### 5. Recommended Tools
• SEO tools  
• Content and design tools  
• Analytics and tracking tools  

### 6. Website / App Recommendations
• What to build if missing  
• UX and conversion optimization  

### 7. 3–6 Month Growth Roadmap
• Month-wise action plan  
• Key KPIs to track  

### Target Audience Segments
• Segments based on business and location  
• Demographics, interests, behaviors  

====
FINAL SUMMARY TABLE

Provide a summary table at the end:

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

Ensure the response is complete and does not stop early.
"""

    try:
        response = client.responses.create(
        model="gpt-5-nano",   
        input=final_prompt,
        max_output_tokens=4000
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
