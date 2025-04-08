# vector_store.py
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        # Use a lightweight model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectors = []
        self.content = []
        
    def add_items(self, items):
        """Add items to the vector store"""
        for item in items:
            embedding = self.model.encode(item["text"])
            self.vectors.append(embedding)
            self.content.append(item)
    
    def search(self, query, top_k=5):
        """Search for most relevant items"""
        query_vector = self.model.encode(query)
        similarities = []
        
        for vec in self.vectors:
            # Calculate cosine similarity
            similarity = np.dot(query_vector, vec) / (np.linalg.norm(query_vector) * np.linalg.norm(vec))
            similarities.append(similarity)
        
        # Get indices of top_k most similar items
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        return [self.content[i] for i in top_indices]
