# Idea Evaluation of Circular Economy Ideas

## Methods

Our project is an idea evaluation system which leverages generative AI to assess business ideas for circular economy. This system assists businesses by evaluating solutions to enable efficient use of time and resources in idea screening. It replicates the thought process of internal teams, shortening the list of ideas under consideration and accelerating decision making. Our system allows a business to input potential solutions along with a customized rubric. It then uses LLMs to emulate various expert perspectives, with each viewpoint evaluating the idea and outputting scores and reasoning. These scores are aggregated to produce a final rating displayed on the UI. We prompt different LLMs to act as domain experts related to the problem area (Fashion, Water, etc.) as well as technical experts like Software Engineers, UX Designers, Product Managers, and more. Users can adjust the weights of these perspectives, emphasizing certain viewpoints over others using the sliders on our website.

## Run

### Clone repository
```bash
git clone https://github.com/syyunn/oai-rag
cd ai_earth_hack
```

### Prep Env & Install dependencies

```bash
conda create -n oai-rag python=3.9
conda activate oai-rag
pip install -r requirements.txt
```

### Replace the API key in the .env file

Create a file named `.env` and add the `OPENAI_API_KEY` to it.

### Run the app

```bash
sudo hupper -m streamlit run app.py
```
