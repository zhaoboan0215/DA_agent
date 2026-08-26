"""Final fixer: replace [Da] with correct char based on project-specific dictionary."""
import re, sys

# Complete mapping of corrupted → correct for common project identifiers
CORRECTIONS = {
    # Copyright header
    'Copyrigh[Da] 2025-pre[Da]en[Da] [Da][Da][Da][Da][Da]AI, Inc.': 'Copyright 2025-present DatusAI, Inc.',
    'Licen[Da]ed [Da]nder [Da]he Ap[Da]che Licen[Da]e, Ver[Da]ion 2.0.': 'Licensed under the Apache License, Version 2.0.',
    'h[Da][Da]p://www.[Da]p[Da]che.org/licen[Da]e[Da]/LICENSE-2.0 for de[Da][Da]il[Da].': 'http://www.apache.org/licenses/LICENSE-2.0 for details.',

    # Python keywords
    'impor[Da]': 'import', 'cl[Da][Da][Da]': 'class', 'def ': 'def ', 're[Da][Da]rn': 'return',
    '[Da]ry': 'try', 'excep[Da]': 'except', 'eli[Da]': 'elit', 'elif ': 'elif ',
    'rai[Da]e': 'raise', 'p[Da][Da][Da]': 'pass', '[Da]ield': 'yield',
    'F[Da]l[Da]e': 'False', 'Tr[Da]e': 'True', 'None': 'None',
    '[Da]elf': 'self', 'proper[Da]y': 'property',

    # Built-in types
    'in[Da]': 'int', 'flo[Da][Da]': 'float', '[Da][Da]r': 'str',
    'Li[Da][Da]': 'List', '[Da]ic[Da]': 'Dict', 'Op[Da]ion[Da]l': 'Optional',
    'bool': 'bool', '[Da]yping': 'typing', 'Any': 'Any',

    # Common functions
    'prin[Da]': 'print', 'en[Da]mer[Da][Da]e': 'enumerate',
    'l[Da]mbd[Da]': 'lambda', 'r[Da]nge': 'range', 'len': 'len',
    'ge[Da]': 'get', '[Da]e[Da][Da][Da][Da]r': 'setattr', 'ge[Da][Da][Da][Da]r': 'getattr',
    'ro[Da]nd': 'round', 'fi[Da]': 'fit', 'Fi[Da]': 'Fit',

    # Common modules
    '[Da]y[Da]': 'sys', '[Da]rgp[Da]r[Da]e': 'argparse',
    'd[Da][Da]e[Da]ime': 'datetime', 're': 're',
    'numpy': 'numpy', 'np': 'np',

    # Project-specific
    'd[Da][Da][Da]engineer': 'dataengineer', 'embedding_model[Da]': 'embedding_models',
    'ge[Da]_doc[Da]men[Da]_embedding_model': 'get_document_embedding_model',
    'doc[Da]men[Da]_[Da][Da]ore': 'document_store',
    'doc[Da]men[Da][Da]ore': 'document_store',
    '[Da]e[Da]rch_doc[Da]': 'search_docs', '[Da]e[Da]rch': 'search',
    'Se[Da]rchRe[Da][Da]l[Da]': 'SearchResult', 'Rec[Da]llConfig': 'RecallConfig',
    'Op[Da]imizedRec[Da]ll': 'OptimizedRecall', 'Q[Da]eryExp[Da]nder': 'QueryExpander',
    '[Da]iver[Da]i[Da]yScorer': 'DiversityScorer', 'BM25': 'BM25',
    '_q[Da]ery_exp[Da]nder': '_query_expander', '_diver[Da]i[Da]y_[Da]corer': '_diversity_scorer',
    '_embedding_model': '_embedding_model', '_[Da][Da]ore': '_store',
    '_[Da]pply_boo[Da][Da]ing': '_apply_boosting', '[Da]o_dic[Da]': 'to_dict',

    # Scores/weights
    'vec[Da]or_[Da]core': 'vector_score', '[Da]ex[Da]_[Da]core': 'text_score',
    '[Da]i[Da]le_boo[Da][Da]': 'title_boost', 'hier[Da]rchy_boo[Da][Da]': 'hierarchy_boost',
    'keyword[Da]_boo[Da][Da]': 'keywords_boost', 'fin[Da]l_[Da]core': 'final_score',
    'vec[Da]or_weigh[Da]': 'vector_weight', '[Da]ex[Da]_weigh[Da]': 'text_weight',
    '[Da]i[Da]le_weigh[Da]': 'title_weight', 'hier[Da]rchy_weigh[Da]': 'hierarchy_weight',
    'keyword[Da]_weigh[Da]': 'keywords_weight',

    # Config
    'exp[Da]nd_q[Da]ery': 'expand_query', 'exp[Da]n[Da]ion_[Da]erm[Da]': 'expansion_terms',
    'en[Da]ble_rer[Da]nk': 'enable_rerank', 'rer[Da]nk_[Da]op_k': 'rerank_top_k',
    'fin[Da]l_[Da]op_k': 'final_top_k', 'm[Da]x_ch[Da]nk[Da]_per_doc': 'max_chunks_per_doc',
    'm[Da]x_per_doc': 'max_per_doc', 'diver[Da]i[Da]y_dec[Da]y': 'diversity_decay',
    'bm25_k1': 'bm25_k1', 'bm25_b': 'bm25_b',

    # Doc structure
    'ch[Da]nk_id': 'chunk_id', 'ch[Da]nk_[Da]ex[Da]': 'chunk_text',
    'ch[Da]nk_index': 'chunk_index', '[Da]i[Da]le': 'title',
    '[Da]i[Da]le[Da]': 'titles', 'n[Da]v_p[Da][Da]h': 'nav_path',
    'gro[Da]p_n[Da]me': 'group_name', 'hier[Da]rchy': 'hierarchy',
    'ver[Da]ion': 'version', '[Da]o[Da]rce_[Da]ype': 'source_type',
    '[Da]o[Da]rce_[Da]rl': 'source_url', 'doc_p[Da][Da]h': 'doc_path',
    'keyword[Da]': 'keywords', 'keyword': 'keyword',

    # Search/Retrieval
    'SELECT_FIEL[Da]S': 'SELECT_FIELDS', '[Da]elec[Da]_field[Da]': 'select_fields',
    're[Da]riev[Da]l': 'retrieval', 'm[Da][Da]ch': 'match',
    'm[Da][Da]ching': 'matching', 'rer[Da]nk': 'rerank', 'rer[Da]nking': 'reranking',
    'diver[Da]i[Da]y': 'diversity', 'q[Da]ery': 'query', 'q[Da]erie[Da]': 'queries',
    'exp[Da]nd': 'expand', 'exp[Da]nded': 'expanded', 'exp[Da]nder': 'expander',
    'exp[Da]n[Da]ion': 'expansion', '[Da]ynonym': 'synonym', '[Da]ynonym[Da]': 'synonyms',
    '[Da]imil[Da]r': 'similar', '[Da]imil[Da]ri[Da]y': 'similarity',
    'b[Da][Da]eline': 'baseline', 'comp[Da]re': 'compare', 'comp[Da]ri[Da]on': 'comparison',

    # Document-related
    'doc[Da]men[Da]': 'document', 'doc[Da]men[Da][Da]': 'documents',
    'doc[Da]men[Da][Da]ion': 'documentation', 'pl[Da][Da]form': 'platform',
    '[Da]crip[Da][Da]': 'scripts', '[Da]crip[Da]': 'script',
    'op[Da]imize': 'optimize', 'op[Da]imized': 'optimized',
    'op[Da]imiza[Da]ion': 'optimization', 'rec[Da]ll': 'recall',
    'ev[Da]l[Da][Da]e': 'evaluate', 'ev[Da]l[Da][Da]ion': 'evaluation',
    'S[Da]r[Da][Da]egy': 'Strategy', '[Da][Da]r[Da][Da]egie[Da]': 'strategies',

    # Common English
    '[Da]he': 'the', '[Da]hi[Da]': 'this', 'wi[Da]h': 'with',
    'no[Da]': 'not', '[Da]o': 'to', 'for': 'for',
    'ex[Da]ern[Da]l': 'external', 'in[Da]ern[Da]l': 'internal',
    'con[Da]en[Da]': 'content', 'con[Da]en[Da][Da]': 'contents',
    'co[Da]n[Da]': 'count', 'co[Da]n[Da][Da]': 'counts',
    'v[Da]l[Da]e': 'value', 'v[Da]l[Da]e[Da]': 'values',
    'i[Da]em': 'item', 'i[Da]em[Da]': 'items',
    'word': 'word', 'word[Da]': 'words',
    'r[Da]nking': 'ranking', 'r[Da]nk': 'rank',
    '[Da]core': 'score', '[Da]core[Da]': 'scores',
    'weigh[Da]': 'weight', 'weigh[Da][Da]': 'weights',
    'boo[Da][Da]': 'boost', 'boo[Da][Da]ing': 'boosting',
    '[Da]erm': 'term', '[Da]erm[Da]': 'terms',
    'ex[Da]mple': 'example', 'Ex[Da]mple': 'Example',
    'ex[Da]mple[Da]': 'examples', 'Ex[Da]mple[Da]': 'Examples',
    'u[Da]age': 'usage', 'U[Da][Da]ge': 'Usage',
    'ini[Da]': 'init', '__ini[Da]__': '__init__',
    'de[Da]crip[Da]ion': 'description', 'form[Da][Da][Da]er': 'formatter',
    'exi[Da]': 'exit',

    # Special multi-word
    'Arg[Da]men[Da]P[Da]r[Da]er': 'ArgumentParser',
    'Raw[Da]e[Da]crip[Da]ionHelpForm[Da][Da][Da]er': 'RawDescriptionHelpFormatter',
    '[Da]dd_[Da]rg[Da]men[Da]': 'add_argument',
    'p[Da]r[Da]e_[Da]rg[Da]': 'parse_args',
    '[Da]c[Da]ion': 'action', '[Da][Da]ore_[Da]r[Da]e': 'store_true',
    'comp[Da]re_wi[Da]h_b[Da][Da]eline': 'compare_with_baseline',
    'b[Da][Da]eline_re[Da][Da]l[Da][Da]': 'baseline_results',
    'op[Da]imized_re[Da][Da]l[Da][Da]': 'optimized_results',
    'b[Da][Da]eline_id[Da]': 'baseline_ids',
    'op[Da]imized_id[Da]': 'optimized_ids',
    'overl[Da]p_co[Da]n[Da]': 'overlap_count',
    'overl[Da]p_r[Da][Da]io': 'overlap_ratio',
    'b[Da][Da]eline_co[Da]n[Da]': 'baseline_count',
    'op[Da]imized_co[Da]n[Da]': 'optimized_count',
    'b[Da][Da]eline_[Da][Da]mple': 'baseline_sample',
    'op[Da]imized_[Da][Da]mple': 'optimized_sample',
    'new_re[Da][Da]l[Da][Da]': 'new_results',
    're[Da][Da]l[Da]': 'result', 're[Da][Da]l[Da][Da]': 'results',
    '[Da]elec[Da]': 'select', 're[Da]rieve': 'retrieve',
    'r[Da]w_re[Da][Da]l[Da][Da]': 'raw_results',
    'doc_co[Da]n[Da][Da]': 'doc_counts',
    'doc_leng[Da]h': 'doc_length', 'doc_leng[Da]h[Da]': 'doc_lengths',
    '[Da]vg_doc_leng[Da]h': 'avg_doc_length',
    'doc_freq[Da]': 'doc_freqs', 'doc_word[Da]': 'doc_words',
    '[Da]okenize': 'tokenize',
    'con[Da]in[Da]e': 'continue', 'c[Da]rren[Da]': 'current',
    'rever[Da]e': 'reverse', 'lo[Da]d': 'load',
    'overl[Da]p': 'overlap', 'overl[Da]p[Da]': 'overlaps',
    'corp[Da][Da]': 'corpus', 'corp[Da][Da]_[Da]ize': 'corpus_size',
    'n[Da]mer[Da][Da]or': 'numerator', 'denomin[Da][Da]or': 'denominator',
    'dec[Da]y': 'decay', 'pen[Da]l[Da]y': 'penalty',
    'progre[Da][Da]ive': 'progressive', 'm[Da]l[Da]iple': 'multiple',
    'advan[Da]ced': 'advanced', 'incorpo[Da]a[Da]ing': 'incorporating',
    'Combine[Da]': 'Combines', 'U[Da]e[Da]': 'Uses',
    'cro[Da][Da]': 'cross', '[Da]yle': 'style',
    'Reform[Da]l[Da][Da]e[Da]': 'Reformulates', 'c[Da]p[Da][Da]re': 'capture',
    'be[Da][Da]er': 'better', '[Da]em[Da]n[Da]ic': 'semantic',
    'Preven[Da][Da]': 'Prevents', 'Enh[Da]nced': 'Enhanced',
    'Componen[Da]': 'Component', 'Componen[Da][Da]': 'Components',
    'Norm[Da]lize': 'Normalize', 'En[Da]ry': 'Entry', 'Poin[Da]': 'Point',
    'Config[Da]r[Da]ble': 'Configurable', 'd[Da]plic[Da][Da]e': 'duplicate',
    'applie[Da]': 'applies', 'Applie[Da]': 'Applies',
    'bui[Da]ld': 'built', 'def[Da]l[Da]': 'default', 'def[Da]l[Da][Da]': 'defaults',
    '[Da]ddi[Da]ional': 'additional', 'config[Da]r[Da][Da]ion': 'configuration',
    'p[Da]r[Da]me[Da]er': 'parameter', 'p[Da]r[Da]me[Da]er[Da]': 'parameters',
    'fe[Da][Da][Da]re': 'feature', 'fe[Da][Da][Da]re[Da]': 'features',
    'improvemen[Da]': 'improvement', 'improvemen[Da][Da]': 'improvements',
    'cre[Da][Da]e': 'create', 'in[Da]er[Da]': 'insert', 'wri[Da]e': 'write',
    'vir[Da][Da][Da]l': 'virtual', '[Da][Da]ored': 'stored',
    'f[Da]ll': 'full', 'Combin[Da][Da]ion': 'Combination',
    'collec[Da]': 'collect', 'Collec[Da]': 'Collect',
    'Conver[Da]': 'Convert', 'dic[Da]ion[Da]ry': 'dictionary',
    '_ge[Da]_doc_[Da]ex[Da]': '_get_doc_text',
    'ge[Da]_[Da]ll_[Da]core[Da]': 'get_all_scores',
    # DuckDB/Snowflake
    'd[Da]ckdb': 'duckdb', '[Da]nowfl[Da]ke': 'snowflake',
    '[Da]yn[Da][Da]x': 'syntax',
}

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply all known corrections (longest first to avoid partial matches)
    items = sorted(CORRECTIONS.items(), key=lambda x: -len(x[0]))
    for pattern, replacement in items:
        content = content.replace(pattern, replacement)

    # Any remaining standalone [Da] → 't' (most common case)
    content = content.replace('[Da]', 't')

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    remaining = content.count('[Da]')
    print(f"{filepath}: {remaining} [Da] remaining")

    if filepath.endswith('.py'):
        try:
            compile(content, filepath, 'exec')
            print("  OK - Valid Python syntax")
        except SyntaxError as e:
            lines = content.split('\n')
            if e.lineno and e.lineno <= len(lines):
                print(f"  Line {e.lineno}: {lines[e.lineno-1].strip()[:100]}")
            print(f"  Error: {e.msg}")

if __name__ == '__main__':
    for path in sys.argv[1:]:
        fix_file(path)
