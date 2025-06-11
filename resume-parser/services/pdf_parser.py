import PyPDF2
from services.parser_interface import ParserInterface , SectionData
from models.resume import Resume
from utils.file_utils import get_file_extension
import nltk
from nltk import pos_tag, word_tokenize, sent_tokenize , RegexpParser , ne_chunk
from dataclasses import asdict
from collections import Counter
import re
class PDFParser(ParserInterface):    
    """
    PDF Parser implementing the 7-step resume parsing pipeline:
    
    1. validate_and_preprocess() - Validate file integrity and reset stream position
    2. extract_raw_content() - Extract raw text content from PDF file
    3. preprocess_text() - Clean and normalize extracted text
    4. identify_sections() - Identify resume sections (contact, education, experience, skills)
    5. extract_structured_data() - Parse structured data from identified sections
    6. create_resume_object() - Create standardized Resume object from parsed data
    
    Returns:
        Resume: Standardized resume object with parsed data
    """
    def parse(self, file_stream):
        return super().parse(file_stream)
    

    def validate_and_preprocess(self, file_stream):
        """Step 1: Validate file integrity and reset stream position"""
        return file_stream
    
    def extract_raw_content(self, file_stream) -> str:
        file_stream.seek(0)
        reader = PyPDF2.PdfReader(file_stream)
        buf = []
        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                buf.append(txt)
        return "\n".join(buf)
    
    def preprocess_text(self, raw_text: str) -> str:
        """Step 3: Condense multiple blank lines but preserve structure and case."""
        # Collapse more than two new‐lines into exactly two 
        text = re.sub(r'\n{3,}', '\n\n', raw_text)  
        # Optionally strip trailing spaces on each line
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        return text
    
    def identify_sections(self, text: str) -> SectionData:
        """Step 4: Identify sections using NLTK POS tagging"""
        lines = text.split('\n')
        titles = []
        paragraphs = []
        
        for line in lines:
            if not line.strip(): 
                continue
                
            tokens   = word_tokenize(line)
            pos_tags = pos_tag(tokens)
            
            # Count verbs and nouns
            verbs = [tag for word, tag in pos_tags if tag.startswith('VB')]
            nouns = [tag for word, tag in pos_tags if tag.startswith('NN')]
            
            # Titles typically have more nouns than verbs and are shorter
            if len(line) < 50 and len(nouns) >= len(verbs):
                titles.append(line)
            else:
                paragraphs.append(line)
        
        return SectionData(titles=titles, paragraphs=paragraphs)
    
    def extract_structured_data(self, sections: SectionData) -> dict:
        """Step 5: Parse structured data from identified sections"""
        # titles pass through untouched
        titles = sections.titles
        # cluster raw paragraph lines into true paragraphs
        raw_para_lines = sections.paragraphs
        clusters = []
        buf: list[str] = []
        for line in raw_para_lines:
            buf.append(line)
            text = " ".join(buf)
            # flush when we hit a sentence end or multiple sentences
            if text.endswith(('.', '!', '?')) or len(sent_tokenize(text)) > 1:
                clusters.append(text.strip())
                buf = []
        if buf:
            clusters.append(" ".join(buf).strip())
        return {
            'titles'    : titles,
            'paragraphs': clusters
        }
    
    def create_resume_object(self, data: dict) -> Resume:
        """
        Step 6: Create standardized Resume object from parsed data

        – Name via NLTK PERSON named‐entity
        – Email via regex
        – Phone via regex (handles parentheses, spaces, dashes)
        – Hyperlinks via token scan
        – Education: sentences with a 4‐digit year
        – Experience: sentences with job‐keywords
        – Skills/Technologies: top noun‐phrase chunks
        """
        titles     = data['titles']
        paragraphs = data['paragraphs']
        text_blob  = " ".join(titles + paragraphs)

        # 1) NAME: first PERSON entity in titles
        name = None
        title_text = " ".join(titles)
        tree = ne_chunk(pos_tag(word_tokenize(title_text)))
        for subtree in tree.subtrees():
            if getattr(subtree, "label", None) == "PERSON":
                name = " ".join(w for w, t in subtree.leaves())
                break
        if not name and titles:
            name = titles[0]

        # 2) EMAIL: regex
        email_pat = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        )
        m = email_pat.search(text_blob)
        email = m.group(0) if m else None

        # 3) PHONE: regex handles +, (), spaces, dashes; at least 7 digits
        phone_pat = re.compile(
            r'(\+?\d[\d\-\s\(\)]{6,}\d)'
        )
        m = phone_pat.search(text_blob)
        phone = m.group(0) if m else None

        # 4) HYPERLINKS: tokens starting with http
        seen = set()
        hyperlinks = []
        for tok in word_tokenize(text_blob):
            if tok.startswith("http") and tok not in seen:
                seen.add(tok)
                hyperlinks.append(tok)

        # 5) EDUCATION: any sentence containing a 4‐digit year
        education = []
        for sent in sent_tokenize(text_blob):
            if any(tok.isdigit() and len(tok) == 4 for tok in word_tokenize(sent)):
                education.append(sent)

        # 6) EXPERIENCE: sentences containing job‐keywords
        job_keys = {"engineer","developer","manager","analyst","intern","architect","consultant"}
        experience = []
        for sent in sent_tokenize(text_blob):
            words = {w.lower() for w in word_tokenize(sent)}
            if words & job_keys:
                experience.append(sent)

        # 7) SKILLS/TECHNOLOGIES: top noun‐phrase chunks
        grammar = "NP: {<JJ>*<NN.*>+}"
        cp = RegexpParser(grammar)
        noun_phrases = []
        for sent in sent_tokenize(text_blob):
            tags = pos_tag(word_tokenize(sent))
            tree = cp.parse(tags)
            for subtree in tree.subtrees():
                if subtree.label() == "NP":
                    np = " ".join(w for w, t in subtree.leaves()).lower()
                    noun_phrases.append(np)
        top_skills = [np for np, _ in Counter(noun_phrases).most_common(10)]

        # 8) INTRODUCTION: first paragraph
        introduction = paragraphs[0] if paragraphs else None

        return Resume(
            name         = name,
            email        = email,
            phone        = phone,
            education    = education,
            experience   = experience,
            skills       = top_skills,
            introduction = introduction,
            technologies = top_skills.copy(),
            hyperlinks   = hyperlinks
        ).get()
