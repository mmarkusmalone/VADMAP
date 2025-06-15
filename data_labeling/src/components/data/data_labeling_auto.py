from transformers import AutoTokenizer, pipeline
from optimum.onnxruntime import ORTModelForSequenceClassification
import csv

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

def chunkify(text, chunk_size=100):
    return text

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

    input_csv = "/Users/mayamarkus-malone/Documents/VADMAP/data/reddit_posts_clean.csv"
    output_csv = "/Users/mayamarkus-malone/Documents/VADMAP/data/reddit_posts_vad.csv"

    with open(input_csv, "r", encoding="utf-8") as infile, \
         open(output_csv, "w", encoding="utf-8", newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header + ["V", "A", "D"])
        for row in reader:
            text = row[0]
            if text.strip() == "":
                writer.writerow(row + ["", "", ""])
                continue
            model_outputs = onnx_classifier(text)
            vad = vadTransformer(model_outputs)
            if "VAD" in header:
                row[header.index("VAD")] = vad
                writer.writerow(row)
            else:
                writer.writerow(row + [vad])

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

if __name__ == "__main__":
    processEntry({})
