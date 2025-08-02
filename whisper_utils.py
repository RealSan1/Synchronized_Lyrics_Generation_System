
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('BAAI/bge-m3')  # 또는 bge-m3, klue 등

def get_embedding(text):
    return model.encode(text, convert_to_tensor=True)

def find_best_match_mcp(w_line, original_lines, used_originals):
    w_emb = get_embedding(w_line)
    best_score = 0
    best_line = None

    for o_line in original_lines:
        if o_line in used_originals:
            continue
        o_emb = get_embedding(o_line)
        score = util.cos_sim(w_emb, o_emb).item()
        if score > best_score and score > 0.60:
            best_score = score
            best_line = o_line

    return best_line, best_score
