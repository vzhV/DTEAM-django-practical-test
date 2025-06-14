TRANSLATE_CV_PROMPT = """
Translate the following CV fields into {language}. 

Return ONLY a valid JSON object with exactly the same keys as provided in the input.

Rules:
- Translate the values of these top-level fields: "firstname", "lastname", "skills", "projects", "bio".
- In the "contacts" field:
    - ONLY translate the keys "email" and "phone" (to the target language). Their values must NOT be translated or changed.
    - Do NOT translate or alter any other keys or values in "contacts".
- Do NOT add or remove fields.
- Output valid JSON only.

Example input:
{{
  "firstname": "John",
  "lastname": "Smith",
  "skills": "Python, Django",
  "projects": "Test project",
  "bio": "Passionate dev",
  "contacts": {{
    "email": "john@example.com",
    "phone": "+12345678",
    "LinkedIn": "@johnny",
    "GitHub": "jsmith"
  }}
}}

Example output (for Spanish):
{{
  "firstname": "Juan",
  "lastname": "Smith",
  "skills": "Python, Django",
  "projects": "Proyecto de prueba",
  "bio": "Desarrollador apasionado",
  "contacts": {{
    "correo electrónico": "john@example.com",
    "teléfono": "+12345678",
    "LinkedIn": "@johnny",
    "GitHub": "jsmith"
  }}
}}

Input:
{cv_json}
"""
