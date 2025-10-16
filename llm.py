import os
OPENAI_KEY = os.environ.get('OPENAI_API_KEY', None)
if OPENAI_KEY:
    try:
        import openai
        openai.api_key = OPENAI_KEY
    except Exception:
        openai = None
else:
    openai = None

class LLMClient:
    def __init__(self):
        pass

    def explain_recommendation(self, user_id, product, user_history, feature_trace):
        title = product.title or product.id
        recent = ', '.join([h['product_id']+'('+h['type']+')' for h in (user_history or [])[:5]])
        trace = ', '.join([f"{k}={v}" for k,v in (feature_trace or {}).items()])
        prompt = (f"Explain in one concise sentence why the product '{title}' is recommended.\n"
                  f"User recent events: {recent}.\nSignals: {trace}.\nKeep it factual.")
        # call OpenAI if available
        if openai:
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{'role':'system','content':'You are concise.'},
                              {'role':'user','content':prompt}],
                    max_tokens=60,
                    temperature=0.2
                )
                txt = resp['choices'][0]['message']['content'].strip()
                return txt
            except Exception:
                pass
        # fallback
        if feature_trace and feature_trace.get('similarity'):
            return f"We recommend '{title}' because it's similar to items you've interacted with (score {feature_trace.get('similarity')})."
        if recent:
            return f"We recommend '{title}' because you recently interacted with {recent.split(',')[0]}."
        return f"We recommend '{title}' based on your browsing history."
