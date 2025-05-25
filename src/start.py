from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForSequenceClassification
import json
import plotly.express as px
import pandas as pd
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D # Required for 3D plotting

# {Emotion: [V,A,D]}

vadDict = {
    "sadness": [-0.896, -0.424, -0.672],
    "neutral": [0.0, 0.0, 0.0],
    "disappointment": [-0.770, -0.020, -0.328],
    "annoyance": [-0.666, 0.436, -0.316],
    "disapproval": [-0.830, 0.102, -0.266],
    "approval": [0.708, -0.080, 0.778],
    "realization": [0.108, 0.020, 0.672],
    "amusement": [0.858, 0.674, 0.606],
    "joy": [0.960, 0.648, 0.588],
    "optimism": [0.898, 0.130, 0.628],
    "anger": [-0.666, 0.730, 0.314],
    "caring": [0.270, -0.062, 0.000],
    "nervousness": [-0.674, 0.830, -0.518],
    "disgust": [-0.896, 0.550, -0.366],
    "relief": [0.688, -0.444, -0.038],
    "desire": [0.792, 0.384, 0.294],
    "grief": [-0.860, 0.280, -0.052],
    "embarrassment": [-0.714, 0.370, -0.548],
    "fear": [-0.854, 0.680, -0.414],
    "remorse": [-0.794, 0.346, -0.246],
    "admiration": [0.938, 0.166, 0.452],
    "confusion": [-0.490, 0.334, -0.446],
    "excitement": [0.792, 0.368, 0.462],
    "curiosity": [0.500, 0.510, -0.074],
    "pride": [0.458, 0.268, 0.696],
    "love": [0.996, 0.334, 0.234],
    "surprise": [0.228, 0.542, -0.100],
    "gratitude": [0.770, -0.118, 0.220]
}

vadEX = {'2025-10-31': {'Woke but a bit mad still. Spanish. Work. English. ': [0.08829526850207566, 0.09972470554687381, 0.11754263009953912], 'Met with Lauren to eat, she was feeling the effects of the night before because she was krunk, being out of pocket, and behind the dj. I tried to calm.': [0.044916417311880195, 0.001966609244635976, 0.02630111922254778], 'She also saw Carlos, which she texted before and definitely affected my tummy. It made me want to be there even more, but I knew that wasn’t best for me.': [-0.3798993299817233, 0.036704206154682534, -0.13718336373353662], 'Got over it. I was in a good mood on the way back. Last class, had a project with Evan. Super chill.': [0.8211339001962333, 0.3588097758188453, 0.5212261225393997], 'Then I had my first date! Was feeling nervous because I was scared it would be meaningless and mid. I also didn’t know what he looked like really and I didn’t love my WhatsApp pic of him. Got ready for a while though, felt good. Hot.': [-0.2697908890812549, 0.4824318621767047, -0.16654190572059252], 'Met him at Jarucha which was cool and authentic. Felt awkward at first but the conversation flowed easily. One beer felt good, a buzz. Really enjoyed my time with him, getting to know him. It was good chats.': [0.8215248369585268, 0.39458354181045924, 0.4936143928497997], 'I think he was not that attractive to me sadly. Also didn’t have any edge which I think I need— didn’t provoke me to say anything out of pocket, new, or interesting. Just a nice, normal dude. Not for me. And I got too drunk and out of pocket by the end. Saying goodbye really cemented the lack of attraction to me.': [-0.7398126126549234, -0.22482511910685196, -0.4677471531756463], 'Went back to dorm, was going out with Marshall and Quimper but Marshall went to Club Malasaña and Quimper wanted to go with the AdPhi guys. I also wanted to go with the AdPhi guys for the rush of seeing Carlos.': [0.18938030026563943, 0.10872913886152859, 0.08144417003620498], 'Napped. Tried getting Marshall and sister invited, went out. Completely forgot about Marshall in the rush of it all which I still feel bad about. All I can do is not do it again and feel this feeling of guilt.': [-0.7095839584796684, 0.07122072652790662, -0.33314891508036726], 'Anyways, met Quimper at Espit Chupitos. Carlos in doorway. Ignore his fucking ass! Say hi to others.': [-0.5326555766973184, 0.49916477426947875, 0.056773191643685716], "Blake says 'male model' to me and then said Campbell showed him Phratmail. I made a joke about them talking shit and he took it really personally.": [0.21071211102983792, 0.21932293281200801, 0.16874364026643676], 'Teddy was telling Quimp & I we were his fav girl friend group, he hates the other group. Quimp and I felt super uncomfortable and out of place. It was funny even in the moment though.': [0.5784129642895987, 0.5447331620123338, 0.4260637756605568], 'People left and we get in a car with Teddy. Lit vibes. In line with the SNu guys, also good chats.': [0.7872140523619191, 0.12671467579762385, 0.44735090286238693], 'Also at Chupitos the tension between Carlos and I was suffocating I think for us both. In line I saw him flirting with a random bitch, take out cigs (degen) and he had a mustache… 3/3.': [-0.03258513506338692, 0.030999351282698664, -0.0012746751807714827], 'Got in, took shots and Red Bull. Carlos was lurky when we were around the table then Quimp and I propelled ourselves into our own choreographed dance world. It was so much motherfucking fun. Time flow. Carlos validation was pulsing. He was staring no joke. On way back from the bathroom, I said ‘awkward’ to him and he laughed and lit up a bit.': [0.8015422254863632, 0.5852628947218786, 0.5362365166720712], 'Went back around 4. Good night. Rubicon.': [0.7081792491294533, 0.1499371207890677, 0.47693372872937184], "Wrote this when going to bed: 'Emotional night so I want to edit. I am confused missing Carlos with us meant to be (which he probably makes every girl think). I feel bad for all the attention I didn’t give him (only said one word) but I’m seriously strong for that shit. I will wake up and be happy. Good night. Quimper funny.'": [-0.19574343715916834, 0.1677788332364189, -0.08807744206200305], 'Ha—my take now is that there is a tension/connection from what is wrapped up in our history between us. It will always be there. Means nothing about us now or our future. He made me miserable!': [-0.4380615357974904, -0.006724198180745462, -0.21614233149848697]}}

def chunkify(text, chunk_size=100):
    return text

def preProcessEntry(journal):
    # end result: {date: {chunk: []}}
    #enters chunked
    processed = {}
    for date, chunks in journal.items():
        processed[date] = {}
        for chunk in chunks:
            processed[date][chunk] = []  # or [0, 0, 0] or any initial list
    return processed

def processEntry(map):
    #sentences = ["I think he was not that attractive to me sadly. Also didn’t have any edge which I think I need— didn’t provoke me to say anything out of pocket, new, or interesting. Just a nice, normal dude. Not for me. "]
    model_id = "SamLowe/roberta-base-go_emotions-onnx"
    file_name = "onnx/model_quantized.onnx"

    model = ORTModelForSequenceClassification.from_pretrained(model_id, file_name=file_name)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    onnx_classifier = pipeline(
        task="text-classification",
        model=model,
        tokenizer=tokenizer,
        top_k=None,
        function_to_apply="sigmoid",  # optional as is the default for the task
    )

    for date in map:
        for chunk in map[date]:
            model_outputs = onnx_classifier(chunk)
            vad = vadTransformer(model_outputs)
            map[date][chunk] = vad
            #map[date][chunk] = model_outputs
    return map

def vadTransformer(model_outputs):
    # model_outputs: list of dicts with 'label' and 'score'
    # returns: dict with weighted average V, A, D
    total_score = 0.0
    vad_sum = [0.0, 0.0, 0.0]
    for output in model_outputs[0]:
        label = output['label']
        score = output['score']
        if label in vadDict:
            v, a, d = vadDict[label]
            vad_sum[0] += v * score
            vad_sum[1] += a * score
            vad_sum[2] += d * score
            total_score += score
    if total_score > 0:
        weighted_vad = [x / total_score for x in vad_sum]
    else:
        weighted_vad = [0.0, 0.0, 0.0]
    return [weighted_vad[0], weighted_vad[1], weighted_vad[2]]

def visualize_with_plotly(data_map):
    plot_data_list = []
    for date, entries in data_map.items():
        for sentence_chunk, vad_scores in entries.items():
            if isinstance(vad_scores, list) and len(vad_scores) == 3:
                plot_data_list.append({
                    'text_chunk': sentence_chunk,
                    'V': vad_scores[0],
                    'A': vad_scores[1],
                    'D': vad_scores[2],
                    'date': date
                })

    if not plot_data_list:
        print("No valid data for Plotly visualization.")
        return
    
    df = pd.DataFrame(plot_data_list)

    fig = px.scatter_3d(df, x='V', y='A', z='D',
                        color='date',  # Optional: color points by date
                        hover_name='text_chunk', # Show the text chunk on hover
                        title='Interactive 3D VAD Score Visualization')

    # Ensure axes are labeled correctly and ranges are set
    fig.update_layout(
        scene=dict(
            xaxis_title='Valence',
            yaxis_title='Arousal',
            zaxis_title='Dominance',
            xaxis=dict(range=[-1,1]),
            yaxis=dict(range=[-1,1]),
            zaxis=dict(range=[-1,1])
        )
    )
    fig.show()

# def visualize(data_map):
#     """
#     Visualizes the VAD (Valence, Arousal, Dominance) scores on a 3D scatter plot.

#     Args:
#         data_map (dict): A dictionary where keys are dates (str) and values are
#                          dictionaries. These inner dictionaries have sentences/chunks (str)
#                          as keys and 3D VAD score lists ([V, A, D]) as values.
#                          Example: {'2025-10-31': {'Sentence1': [v1,a1,d1], ...}}
#     """
#     fig = plt.figure(figsize=(12, 10))
#     ax = fig.add_subplot(111, projection='3d')

#     all_v = []
#     all_a = []
#     all_d = []
#     # Sentences/chunks could be collected here for advanced annotations or hover effects
#     # with other libraries, but for a basic matplotlib plot, we'll keep it simple.

#     for date, entries in data_map.items():
#         for chunk, vad_scores in entries.items():
#             if isinstance(vad_scores, list) and len(vad_scores) == 3:
#                 all_v.append(vad_scores[0])
#                 all_a.append(vad_scores[1])
#                 all_d.append(vad_scores[2])
#             else:
#                 print(f"Warning: Skipping invalid VAD scores for chunk on {date}: {vad_scores}")

#     if not all_v: # No data to plot
#         print("No valid VAD data to visualize.")
#         ax.set_title('No VAD Data to Display')
#         plt.show()
#         return 0 # Indicate no plot was generated or data was missing

#     # Create the 3D scatter plot
#     ax.scatter(all_v, all_a, all_d, c='skyblue', s=60, edgecolors='k', alpha=0.7)

#     ax.set_xlabel('Valence (V)')
#     ax.set_ylabel('Arousal (A)')
#     ax.set_zlabel('Dominance (D)')
#     ax.set_title('3D Visualization of VAD Scores for Journal Chunks')

#     # VAD scores are typically in the range [-1, 1]
#     ax.set_xlim([-1, 1])
#     ax.set_ylim([-1, 1])
#     ax.set_zlim([-1, 1])

#     plt.tight_layout() # Adjust layout to make sure everything fits without overlapping
#     plt.show()
#     return 1 # Indicate success


def caller(journal):
    #map the json journal to a dictionary key:date, value: {chunk: []}
    map = preProcessEntry(journal)
    #populate the map with the VAD scores
    popMap = processEntry(map)
    return popMap


if __name__ == "__main__":
    journal = []
    with open('journals/firsTest.json', 'r') as file:
        journal = json.load(file)

    # this journal is pre chunked, will have to be chunked before
    #map = caller(journal)

    # print(f"Processed VAD data for {len(vadEX)} dates.")
    # first_date_key = list(vadEX.keys())[0] if vadEX else None
    # if first_date_key:
    #     num_chunks_first_date = len(vadEX[first_date_key])
    #     print(f"First date '{first_date_key}' has {num_chunks_first_date} text chunks.")
    # visualize(vadEX)

    visualize_with_plotly(vadEX)