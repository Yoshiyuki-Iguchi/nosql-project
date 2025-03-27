'''
This one is used to select  a method for different number of entries

'''

import json
import random
from neo4j import GraphDatabase

# Specify the path to your JSON file
file_path = '/Users/yoshiyukiiguchi/Desktop/mads_semestre1/nosql/project/proteins.json'  # Replace with the correct path if necessary

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)


class ProteinGraphless1000:
    '''
    I will used this section if my number of nodes are less than 500
    '''
    def __init__(self, data, num, alpha, uri="bolt://localhost:7687", user="neo4j", password="propro_8888"):
        self.data = data  # The data containing proteins and their domains
        self.num = num    # Number of proteins to select
        self.alpha = alpha  # Threshold for similarity
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def refresh_graph(self):
        """
        Clear all nodes and relationships in the database.
        """
        session = self.driver.session()
        try:
            session.run("MATCH (n) DETACH DELETE n")  # Clears the entire graph
        finally:
            session.close()

    def select_proteins(self):
        """
        Select a random sample of proteins from the data.
        """
        return random.sample(self.data, self.num)

    def extract_nodes(self, proteins_selected):
        """
        Extract tuples of protein entries and their corresponding domain sets.
        """
        nodes = [(entry["Entry"], set(entry.get("InterPro", "").strip(";").split(";"))) for entry in proteins_selected]
        return nodes

    def calculate_jaccard_similarity(self, domains1, domains2):
        """
        Calculate the Jaccard similarity between two sets of domains.
        """
        inter = len(domains1.intersection(domains2))
        un = len(domains1.union(domains2))
        return inter / un if un > 0 else 0.0

    def similarity_nodes(self, nodes):
        """
        Calculate the Jaccard similarity for each pair of proteins and return edges 
        that have similarity above the threshold alpha.
        """
        graph = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):  # To avoid repeating pairs
                protein1, domains1 = nodes[i]
                protein2, domains2 = nodes[j]

                # Skip calculation if either protein has an empty or invalid domain set
                if not domains1 or '' in domains1 or not domains2 or '' in domains2:
                    similarity = 0.0
                else:
                    similarity = self.calculate_jaccard_similarity(domains1, domains2)

                # Add the pair to the graph if similarity exceeds the threshold
                if similarity > self.alpha:
                    graph.append([protein1, protein2, similarity])

        return graph

    def create_neo4j_graph(self, graph, proteins_selected):
        """
        Create nodes and relationships in Neo4j based on the generated protein similarity graph.
        """
        session = self.driver.session()
        try:
            # Create nodes for all proteins, even if they do not have high similarity
            for protein in proteins_selected:
                session.run(""" 
                    MERGE (p:Protein {entry: $entry})
                    SET p.entry_name = $entry_name,
                        p.protein_names = $protein_names,
                        p.gene_names = $gene_names,
                        p.organism = $organism,
                        p.sequence = $sequence,
                        p.interpro = $interpro
                """, 
                entry=protein["Entry"],
                entry_name=protein.get("Entry Name", ""),
                protein_names=protein.get("Protein names", ""),
                gene_names=protein.get("Gene Names", ""),
                organism=protein.get("Organism", ""),
                sequence=protein.get("Sequence", ""),
                interpro=protein.get("InterPro", "")
                )
            
            # Create relationships only for proteins that have similarity above the threshold
            for protein1, protein2, similarity in graph:
                session.run(""" 
                    MATCH (p1:Protein {entry: $entry1}), (p2:Protein {entry: $entry2})
                    MERGE (p1)-[r:SIMILAR_TO]->(p2)
                    SET r.similarity = $similarity
                """, entry1=protein1, entry2=protein2, similarity=similarity)

        finally:
            session.close()

    def generate_protein_graph(self):
        """
        Full workflow to generate a protein similarity graph based on selected proteins.
        """
        self.refresh_graph()  # Clear previous data
        proteins_selected = self.select_proteins()  # Select proteins randomly
        nodes = self.extract_nodes(proteins_selected)  # Extract nodes
        graph = self.similarity_nodes(nodes)  # Calculate similarities and generate the graph
        self.create_neo4j_graph(graph, proteins_selected)  # Push the data to Neo4j
        return graph

class ProteinGraph1000:
    '''
    Used this code if number of entries are greater than 500
    '''
    def __init__(self, data, num, alpha, uri="bolt://localhost:7687", user="neo4j", password="propro_8888"):
        self.data = data  # The data containing proteins and their domains
        self.num = num    # Number of proteins to select
        self.alpha = alpha  # Threshold for similarity
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def refresh_graph(self):
        """
        Clear all nodes and relationships in the database.
        """
        session = self.driver.session()
        try:
            session.run("MATCH (n) DETACH DELETE n")  # Clears the entire graph
        finally:
            session.close()

    def select_proteins(self):
        """
        Select a random sample of proteins from the data.
        """
        return random.sample(self.data, self.num)

    def extract_nodes(self, proteins_selected):
        """
        Extract tuples of protein entries and their corresponding domain sets.
        """
        nodes = [(entry["Entry"], set(entry.get("InterPro", "").strip(";").split(";"))) for entry in proteins_selected]
        return nodes

    def calculate_jaccard_similarity(self, domains1, domains2):
        """
        Calculate the Jaccard similarity between two sets of domains.
        """
        inter = len(domains1.intersection(domains2))
        un = len(domains1.union(domains2))
        return inter / un if un > 0 else 0.0

    def similarity_nodes(self, nodes):
        """
        Calculate the Jaccard similarity for each pair of proteins and return edges 
        that have similarity above the threshold alpha.
        """
        graph = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):  # To avoid repeating pairs
                protein1, domains1 = nodes[i]
                protein2, domains2 = nodes[j]

                # Skip calculation if either protein has an empty or invalid domain set
                if not domains1 or '' in domains1 or not domains2 or '' in domains2:
                    similarity = 0.0
                else:
                    similarity = self.calculate_jaccard_similarity(domains1, domains2)

                # Add the pair to the graph if similarity exceeds the threshold
                if similarity > self.alpha:
                    graph.append([protein1, protein2, similarity])

        return graph

    def create_neo4j_graph(self, graph, proteins_selected):
        """
        Create nodes and relationships in Neo4j based on the generated protein similarity graph.
        Now including detailed properties for each protein node.
        """
        session = self.driver.session()
        try:
            for protein1, protein2, similarity in graph:
                # Find the protein data based on the Entry
                protein1_data = next((entry for entry in proteins_selected if entry["Entry"] == protein1), {})
                protein2_data = next((entry for entry in proteins_selected if entry["Entry"] == protein2), {})
                
                # Create nodes with detailed properties (Entry, Entry Name, Protein Names, etc.)
                session.run("""
                    MERGE (p1:Protein {entry: $entry1})
                    SET p1.entry_name = $entry_name1,
                        p1.protein_names = $protein_names1,
                        p1.gene_names = $gene_names1,
                        p1.organism = $organism1,
                        p1.sequence = $sequence1,
                        p1.interpro = $interpro1
                """, 
                entry1=protein1,
                entry_name1=protein1_data.get("Entry Name", ""),
                protein_names1=protein1_data.get("Protein names", ""),
                gene_names1=protein1_data.get("Gene Names", ""),
                organism1=protein1_data.get("Organism", ""),
                sequence1=protein1_data.get("Sequence", ""),
                interpro1=protein1_data.get("InterPro", "")
                )
                
                session.run("""
                    MERGE (p2:Protein {entry: $entry2})
                    SET p2.entry_name = $entry_name2,
                        p2.protein_names = $protein_names2,
                        p2.gene_names = $gene_names2,
                        p2.organism = $organism2,
                        p2.sequence = $sequence2,
                        p2.interpro = $interpro2
                """, 
                entry2=protein2,
                entry_name2=protein2_data.get("Entry Name", ""),
                protein_names2=protein2_data.get("Protein names", ""),
                gene_names2=protein2_data.get("Gene Names", ""),
                organism2=protein2_data.get("Organism", ""),
                sequence2=protein2_data.get("Sequence", ""),
                interpro2=protein2_data.get("InterPro", "")
                )
                
                # Create a relationship if similarity is above the threshold
                session.run("""
                    MATCH (p1:Protein {entry: $entry1}), (p2:Protein {entry: $entry2})
                    MERGE (p1)-[r:SIMILAR_TO]->(p2)
                    SET r.similarity = $similarity
                """, entry1 = protein1, entry2 = protein2, similarity=similarity)
        finally:
            session.close()

    def generate_protein_graph(self):
        """
        Full workflow to generate a protein similarity graph based on selected proteins.
        """
        self.refresh_graph()  # Clear previous data
        proteins_selected = self.select_proteins()  # Select proteins
        nodes = self.extract_nodes(proteins_selected)  # Extract nodes
        graph = self.similarity_nodes(nodes)  # Calculate similarities and generate the graph
        self.create_neo4j_graph(graph, proteins_selected)  # Push the data to Neo4j
        return graph


# Create an instance of ProteinGraph
def which_method(num,alpha):
    '''
    num = The num entries wanted
    alpha = Is the threshold
    '''
    if num > 1000:
        protein_graph = ProteinGraph1000(data, num, alpha)
    else:
       protein_graph = ProteinGraphless1000(data, num, alpha)
    
    return protein_graph
    

protein_graph = which_method(1000,0.0)
# Generate the protein graph for the selected random proteins
graph = protein_graph.generate_protein_graph()

# Print the generated graph (can be large, consider modifying this for better output handling)
print(graph)
print(len(graph))
