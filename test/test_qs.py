import requests
import json

def test_q0():
    url = f"http://127.0.0.1:5000/api/parse/"
    r = requests.post(url, json="What drugs affect Ebola?")
    graph = r.json()
    assert 'nodes' in graph
    assert 'edges' in graph
    assert len(graph['nodes'])==2
    assert len(graph['edges'])==1
    names = [n['name'] if 'name' in n else None for n in graph['nodes']]
    assert 'Ebola hemorrhagic fever' in names
    ebola_idx = names.index('Ebola hemorrhagic fever')
    ebola_node = graph['nodes'][ebola_idx]
    # assert ebola_node['type'] == 'disease'
    types = [n['type'] if 'type' in n else None for n in graph['nodes']]
    assert 'chemical_substance' in types
    drug_idx = types.index('chemical_substance')
    drug_node = graph['nodes'][drug_idx]
    assert graph['edges'][0]['source_id'] == drug_node['id']
    assert graph['edges'][0]['target_id'] == ebola_node['id']
    assert graph['edges'][0]['predicate'] == 'affects'

def test_q1():
    url = f"http://127.0.0.1:5000/api/parse/"
    r = requests.post(url, json="What drugs are affected by Ebola?")
    graph = r.json()
    assert 'nodes' in graph
    assert 'edges' in graph
    assert len(graph['nodes'])==2
    assert len(graph['edges'])==1
    names = [n['name'] if 'name' in n else None for n in graph['nodes']]
    assert 'Ebola hemorrhagic fever' in names
    ebola_idx = names.index('Ebola hemorrhagic fever')
    ebola_node = graph['nodes'][ebola_idx]
    # assert ebola_node['type'] == 'disease'
    types = [n['type'] if 'type' in n else None for n in graph['nodes']]
    assert 'chemical_substance' in types
    drug_idx = types.index('chemical_substance')
    drug_node = graph['nodes'][drug_idx]
    assert graph['edges'][0]['source_id'] == drug_node['id']
    assert graph['edges'][0]['target_id'] == ebola_node['id']
    assert graph['edges'][0]['predicate'] == 'is affected by'

def test_q2():
    url = f"http://127.0.0.1:5000/api/parse/"
    r = requests.post(url, json="What drugs is Ebola affected by?")
    graph = r.json()
    assert 'nodes' in graph
    assert 'edges' in graph
    assert len(graph['nodes'])==2
    assert len(graph['edges'])==1
    names = [n['name'] if 'name' in n else None for n in graph['nodes']]
    assert 'Ebola hemorrhagic fever' in names
    ebola_idx = names.index('Ebola hemorrhagic fever')
    ebola_node = graph['nodes'][ebola_idx]
    # assert ebola_node['type'] == 'disease'
    types = [n['type'] if 'type' in n else None for n in graph['nodes']]
    assert 'chemical_substance' in types
    drug_idx = types.index('chemical_substance')
    drug_node = graph['nodes'][drug_idx]
    assert graph['edges'][0]['source_id'] == ebola_node['id']
    assert graph['edges'][0]['target_id'] == drug_node['id']
    assert graph['edges'][0]['predicate'] == 'is affected by'

def test_q3():
    url = f"http://127.0.0.1:5000/api/parse/"
    r = requests.post(url, json="What drugs does Ebola affect?")
    graph = r.json()
    assert 'nodes' in graph
    assert 'edges' in graph
    assert len(graph['nodes'])==2
    assert len(graph['edges'])==1
    names = [n['name'] if 'name' in n else None for n in graph['nodes']]
    assert 'Ebola hemorrhagic fever' in names
    ebola_idx = names.index('Ebola hemorrhagic fever')
    ebola_node = graph['nodes'][ebola_idx]
    # assert ebola_node['type'] == 'disease'
    types = [n['type'] if 'type' in n else None for n in graph['nodes']]
    assert 'chemical_substance' in types
    drug_idx = types.index('chemical_substance')
    drug_node = graph['nodes'][drug_idx]
    assert graph['edges'][0]['source_id'] == ebola_node['id']
    assert graph['edges'][0]['target_id'] == drug_node['id']
    assert graph['edges'][0]['predicate'] == 'affects'