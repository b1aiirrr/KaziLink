"""
KaziLink Opportunity Categorizer
Uses OpenAI GPT-4 to intelligently categorize job postings into:
- Attachment: Industrial/field attachments for current students
- Internship: Graduate trainee programs for recent graduates
- Job: Full-time employment opportunities
"""

import os
from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OpportunityType = Literal['attachment', 'internship', 'job']

class OpportunityCategorizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def categorize(
        self,
        title: str,
        description: str,
        company: str = ""
    ) -> OpportunityType:
        """
        Categorize an opportunity using GPT-4.
        
        Args:
            title: Job title
            description: Full job description
            company: Company name (optional)
            
        Returns:
            'attachment', 'internship', or 'job'
        """
        
        prompt = f"""You are an expert at categorizing job opportunities in Kenya. 
Analyze the following job posting and categorize it into EXACTLY ONE category:

**Categories:**
1. **attachment** - Industrial/field attachments for CURRENT university/college students. These:
   - Require an introduction/attachment letter from the institution
   - Are typically 3-6 months duration
   - Are aimed at students fulfilling academic requirements
   - May be unpaid or stipend-based
   - Keywords: "industrial attachment", "field attachment", "student attachment", "introduction letter required"

2. **internship** - Graduate trainee programs for RECENT graduates. These:
   - Target fresh graduates (0-2 years experience)
   - Are typically 6-12 months duration
   - Often lead to full-time employment
   - Provide structured training programs
   - Keywords: "graduate trainee", "internship program", "fresh graduate", "recent graduate"

3. **job** - Full-time employment positions. These:
   - Require professional work experience
   - Are permanent or long-term contract positions
   - Have competitive salaries
   - Expect immediate contribution
   - Keywords: "2+ years experience", "permanent position", "full-time", "senior", "manager"

**Job Posting:**
Title: {title}
Company: {company}
Description: {description[:1500]}

Respond with ONLY ONE WORD: attachment, internship, or job"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a job classification expert. Respond with only: attachment, internship, or job"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            # Validate response
            if result in ['attachment', 'internship', 'job']:
                return result
            else:
                # Fallback to keyword-based classification
                return self._fallback_categorize(title, description)
                
        except Exception as e:
            print(f"Error categorizing with GPT-4: {e}")
            return self._fallback_categorize(title, description)
    
    def _fallback_categorize(self, title: str, description: str) -> OpportunityType:
        """
        Fallback keyword-based categorization if GPT-4 fails.
        """
        text = f"{title} {description}".lower()
        
        # Attachment keywords (highest priority for students)
        attachment_keywords = [
            'attachment', 'industrial attachment', 'field attachment',
            'introduction letter', 'student', 'undergraduate'
        ]
        
        # Internship keywords
        internship_keywords = [
            'internship', 'intern', 'graduate trainee', 'graduate program',
            'fresh graduate', 'recent graduate', 'trainee'
        ]
        
        # Count keyword matches
        attachment_score = sum(1 for kw in attachment_keywords if kw in text)
        internship_score = sum(1 for kw in internship_keywords if kw in text)
        
        # Determine category
        if attachment_score > 0:
            return 'attachment'
        elif internship_score > 0:
            return 'internship'
        else:
            return 'job'
    
    def batch_categorize(self, opportunities: list[dict]) -> list[dict]:
        """
        Categorize multiple opportunities.
        
        Args:
            opportunities: List of dicts with 'title', 'description', 'company'
            
        Returns:
            Same list with 'type' field added
        """
        for opp in opportunities:
            opp['type'] = self.categorize(
                title=opp.get('title', ''),
                description=opp.get('description', ''),
                company=opp.get('company', '')
            )
        
        return opportunities


# Example usage
if __name__ == "__main__":
    categorizer = OpportunityCategorizer()
    
    # Test cases
    test_cases = [
        {
            "title": "Industrial Attachment - Engineering",
            "description": "We are seeking university students for a 3-month industrial attachment. Students must provide an introduction letter from their institution.",
            "company": "ABC Company"
        },
        {
            "title": "Graduate Trainee Program",
            "description": "Fresh graduates with a degree in Business are invited to join our 12-month trainee program with potential for permanent employment.",
            "company": "XYZ Corporation"
        },
        {
            "title": "Senior Software Engineer",
            "description": "We need an experienced software engineer with 5+ years of experience in Python and Django. This is a permanent position.",
            "company": "Tech Startup"
        }
    ]
    
    for case in test_cases:
        category = categorizer.categorize(
            title=case['title'],
            description=case['description'],
            company=case['company']
        )
        print(f"\nTitle: {case['title']}")
        print(f"Category: {category}")
