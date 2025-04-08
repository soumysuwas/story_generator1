# utils/context_compressor.py
from utils.token_counter import TokenCounter

class ContextCompressor:
    """Utility for compressing context while preserving important information"""
    
    def __init__(self, token_counter=None):
        """Initialize the context compressor"""
        self.token_counter = token_counter or TokenCounter()
    
    def compress_context(self, context, max_tokens=2000):
        """Compress context to fit within max_tokens while preserving important information"""
        if self.token_counter.count_tokens(context) <= max_tokens:
            return context
        
        # Split context into sections
        sections = self._split_into_sections(context)
        
        # Prioritize sections
        prioritized_sections = self._prioritize_sections(sections)
        
        # Compress each section based on priority
        compressed_context = []
        current_tokens = 0
        
        # Always include title and concept (first section)
        first_section = prioritized_sections[0]
        compressed_context.append(first_section)
        current_tokens += self.token_counter.count_tokens(first_section)
        
        # Process remaining sections
        for section in prioritized_sections[1:]:
            section_tokens = self.token_counter.count_tokens(section)
            
            if current_tokens + section_tokens <= max_tokens:
                # Include full section if it fits
                compressed_context.append(section)
                current_tokens += section_tokens
            else:
                # Compress section if needed
                remaining_tokens = max_tokens - current_tokens
                if remaining_tokens > 100:  # Only include if we have enough tokens left
                    compressed_section = self._compress_section(section, remaining_tokens)
                    compressed_context.append(compressed_section)
                    current_tokens += self.token_counter.count_tokens(compressed_section)
                break
        
        return "\n".join(compressed_context)
    
    def _split_into_sections(self, context):
        """Split context into logical sections based on headers"""
        lines = context.split("\n")
        sections = []
        current_section = []
        
        for line in lines:
            if line.startswith("##") or line.startswith("Title:") or line.startswith("Concept:"):
                if current_section:
                    sections.append("\n".join(current_section))
                    current_section = []
            current_section.append(line)
        
        if current_section:
            sections.append("\n".join(current_section))
        
        return sections
    
    def _prioritize_sections(self, sections):
        """Prioritize sections based on importance"""
        # Title and concept are highest priority
        high_priority = [s for s in sections if "Title:" in s or "Concept:" in s]
        # Characters are next priority
        medium_priority = [s for s in sections if "## Characters" in s]
        # Recent events are next
        medium_high_priority = [s for s in sections if "## Recent Events" in s]
        # World information is lowest priority
        low_priority = [s for s in sections if "## World Information" in s]
        # Other sections
        other_sections = [s for s in sections if s not in high_priority + medium_priority + medium_high_priority + low_priority]
        
        return high_priority + medium_priority + medium_high_priority + other_sections + low_priority
    
    def _compress_section(self, section, max_tokens):
        """Compress a single section to fit within max_tokens"""
        lines = section.split("\n")
        header = lines[0] if lines else ""
        content = lines[1:] if len(lines) > 1 else []
        
        # Always keep the header
        compressed = [header]
        current_tokens = self.token_counter.count_tokens(header)
        
        # Add as many content lines as possible
        for line in content:
            line_tokens = self.token_counter.count_tokens(line)
            if current_tokens + line_tokens <= max_tokens:
                compressed.append(line)
                current_tokens += line_tokens
            else:
                break
        
        return "\n".join(compressed)
