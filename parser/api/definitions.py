from parser.api.setup import swagger

@swagger.definition('Graph')
class Graph():
    """
    Graph
    ---
    properties:
      nodes:
        type: "array"
        items:
          $ref: "#/definitions/Node"
      edges:
        type: "array"
        items:
          $ref: "#/definitions/Edge"
    """
    pass
    
@swagger.definition('Node')
class Node():
    """
    Node Object
    ---
    id: Node
    required:
        - id
    properties:
        id:
            type: string
            required: true
        type:
            type: string
        name:
            type: string
        identifiers:
            type: array
            items:
                type: string
            default: []
    """
    pass

@swagger.definition('Edge')
class Edge():
    """
    Edge
    ---
    id: Edge
    required:
        - source_id
        - target_id
    properties:
        type:
            type: "string"
            example: "affects"
            description: "Higher-level relationship type of this edge"
        relation:
            type: "string"
            example: "affects"
            description: "Lower-level relationship type of this edge"
        source_id:
            type: "string"
            example: "http://omim.org/entry/603903"
            description: "Corresponds to the @id of source node of this edge"
        target_id:
            type: "string"
            example: "https://www.uniprot.org/uniprot/P00738"
            description: "Corresponds to the @id of target node of this edge"
        is_defined_by:
            type: "string"
            example: "RTX"
            description: "A CURIE/URI for the translator group that made the KG"
        provided_by:
            type: "string"
            example: "OMIM"
            description: "A CURIE/URI for the knowledge source that defined this edge"
        confidence:
            type: "number"
            format: "float"
            example: 0.99
            description: "Confidence metric for this edge, a value 0.0 (no confidence) and 1.0 (highest confidence)"
        publications:
            type: "string"
            example: "PubMed:12345562"
            description: "A CURIE/URI for publications associated with this edge"
        evidence_type:
            type: "string"
            example: "ECO:0000220"
            description: "A CURIE/URI for class of evidence supporting the statement made in an edge - typically a class from the ECO ontology"
        qualifiers:
            type: "string"
            example: "ECO:0000220"
            description: "Terms representing qualifiers that modify or qualify the meaning of the statement made in an edge"
        negated:
            type: "boolean"
            example: "true"
            description: "Boolean that if set to true, indicates the edge statement is negated i.e. is not true"
    """
    pass
