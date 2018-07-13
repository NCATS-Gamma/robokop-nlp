import os
import requests
from lark import Lark
from nltk.tokenize.casual import casual_tokenize as tokenize

def find_brackets(words):
    depth = 0
    start_idx = []
    end_idx = []
    on_term = False
    for i, word in enumerate(words):
        if word == '[':
            depth += 1
        elif word == ']':
            depth -= 1
        if depth<0:
            raise ValueError("Invalid string: unbalanced brackets.")
        elif depth>0 and not on_term:
            on_term = True
            start_idx.append(i)
        elif depth == 0 and on_term:
            on_term = False
            end_idx.append(i)
    if depth>0:
        raise ValueError("Invalid string: unbalanced brackets.")
    for i, (s, e) in enumerate(zip(reversed(start_idx), reversed(end_idx))):
        words = words[:s] + [' '.join(words[s+1:e])] + words[e+1:]
    return words

def parse_text(text):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_dir, '..', 'known_words.txt')) as file:
        lines = file.read().split('\n')
        words = [l for l in lines if ',' not in l]
        word_map = {l.split(', ')[0]:l.split(', ')[-1] for l in lines if ',' in l}

    text = text.lower()
    original_terms = [word_map[token] if token in word_map else token for token in tokenize(text)]
    bracketed_terms = find_brackets(original_terms)

    # collapse unknown terms
    collapsed_terms = []
    joint_term = []
    for t in bracketed_terms:
        if t in words:
            if joint_term:
                collapsed_terms.append(' '.join(joint_term))
                joint_term = []
            collapsed_terms.append(t)
        else:
            joint_term.append(t)
    if joint_term:
        collapsed_terms.append(' '.join(joint_term))

    term_map = {f'ENTITY{i}':w for i, w in enumerate(collapsed_terms) if w not in words}
    substituted_terms = [w if w in words else f'ENTITY{i}' for i, w in enumerate(collapsed_terms)]
    text = ' '.join(substituted_terms)

    with open(os.path.join(file_dir, '..', 'grammar.txt')) as file:
        grammar = file.read()

    parser = Lark(grammar, start='sentence', ambiguity='explicit')  # Explicit ambiguity in parse tree!

    tree = parser.parse(text)

    graph = parse_tree(tree)

    graph = post_proc_graph(graph, term_map)
    return graph

def parse_noun(noun, id, graph):
    NOUN = noun.children[0] # assume a single noun
    graph['nodes'].append({
        'id': id,
        'name': NOUN.value
    })
    return graph

def parse_nom(nom, id, graph):
    if nom.data == "noun":
        return parse_noun(nom, id, graph)
    

def parse_tree(tree):
    # produce graph with nodes and edges
    graph = {
        'nodes': [],
        'edges': []
    }
    if tree.data == 'q_gc':
        nom = tree.children[0]
        graph = parse_nom(nom, 0, graph)
        graph['edges'].append({
            'source_id': 0,
            'target_id': 1
        })
        graph['nodes'].append({
            'id': 1,
            'name': 'gene'
        })
        graph['edges'].append({
            'source_id': 1,
            'target_id': 2
        })
        graph['nodes'].append({
            'id': 2,
            'name': 'genetic_condition'
        })
    elif tree.data == 'q_cop':
        nom = tree.children[0]
        if nom.data != 'conjunction':
            raise ValueError('Try a question of the form "What is the COP for [drug] and [disease]?".')
        graph = parse_nom(nom.children[0], 0, graph)
        graph['edges'].append({
            'source_id': 0,
            'target_id': 1
        })
        graph['nodes'].append({
            'id': 1,
            'name': 'gene'
        })
        graph['edges'].append({
            'source_id': 1,
            'target_id': 2
        })
        graph['nodes'].append({
            'id': 2,
            'name': 'biological_process'
        })
        graph['edges'].append({
            'source_id': 2,
            'target_id': 3
        })
        graph['nodes'].append({
            'id': 3,
            'name': 'cell'
        })
        graph['edges'].append({
            'source_id': 3,
            'target_id': 4
        })
        graph['nodes'].append({
            'id': 4,
            'name': 'anatomical_entity'
        })
        graph['edges'].append({
            'source_id': 4,
            'target_id': 5
        })
        graph['nodes'].append({
            'id': 5,
            'name': 'phenotypic_feature'
        })
        graph['edges'].append({
            'source_id': 5,
            'target_id': 6
        })
        graph = parse_nom(nom.children[2], 6, graph)
    elif tree.data == 'q_what_0':
        if tree.children[2].data == "passive":
            nom = tree.children[-3]
            graph = parse_nom(nom, 0, graph)

            obj = tree.children[2].children[1]
            pp = obj.children[1]

            preposition = pp.children[0]
            verb = obj.children[0]
            graph['edges'].append({
                'source_id': 0,
                'target_id': 1,
                'predicate': f"is {verb.value} {preposition.value}"
            })

            nom = pp.children[1]
            graph = parse_nom(nom, 1, graph)
        else:
            nom = tree.children[-3]
            graph = parse_nom(nom, 0, graph)

            vp = tree.children[-2]
            verb = vp.children[0]
            graph['edges'].append({
                'source_id': 0,
                'target_id': 1,
                'predicate': verb.value
            })

            nom = vp.children[1]
            graph = parse_nom(nom, 1, graph)
    elif tree.data == 'q_what_1':
        nom = tree.children[-3]
        graph = parse_nom(nom, 0, graph)

        verb = tree.children[-2]
        graph['edges'].append({
            'source_id': 0,
            'target_id': 1,
            'predicate': verb.value
        })

        nom = tree.children[1]
        graph = parse_nom(nom, 1, graph)
    elif tree.data == 'q_what_2':
        obj = tree.children[-2]
        pp = obj.children[1]

        nom = tree.children[1]
        graph = parse_nom(nom, 0, graph)

        verb = obj.children[0]
        preposition = pp.children[0]
        graph['edges'].append({
            'source_id': 0,
            'target_id': 1,
            'predicate': f"is {verb.value} {preposition.value}"
        })

        nom = pp.children[1]
        graph = parse_nom(nom, 1, graph)
    elif tree.data == 'q_what_3':
        nom = tree.children[-4]
        graph = parse_nom(nom, 0, graph)

        adjective = tree.children[-3]
        preposition = tree.children[-2]
        graph['edges'].append({
            'source_id': 0,
            'target_id': 1,
            'predicate': f"is {adjective.value} {preposition.value}"
        })

        nom = tree.children[1]
        graph = parse_nom(nom, 1, graph)

    return graph

def post_proc_graph(graph, term_map):
    for n in graph['nodes']:
        if n['name'] in term_map:
            n['name'] = term_map[n['name']]
            # bionames_query = f"http://127.0.0.1:5001/lookup/{n['name']}/{{concept}}/"
            bionames_query = f"https://bionames.renci.org/lookup/{n['name']}/{{concept}}/"
            response = requests.get(bionames_query).json()
            first = response[0]
            n['curie'] = first['id']
            n['name'] = first['label'] if 'label' in first else first['id']
            if 'type' in n:
                n['type'] = first['type']
        else:
            n['type'] = n['name']
            n.pop('name')
            
    return graph

if __name__=='__main__':
    try:
        parse_text("What genes affect Ebola?")
    except Exception as err:
        print(f'Failed to parse: {err}')

    try:
        parse_text("What cells are affected by Ebola?")
    except Exception as err:
        print(f'Failed to parse: {err}')

    try:
        parse_text("What genes is Ebola affected by?")
    except Exception as err:
        print(f'Failed to parse: {err}')

    try:
        parse_text("What cells does Ebola affect?")
    except Exception as err:
        print(f'Failed to parse: {err}')