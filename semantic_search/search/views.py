from django.shortcuts import render
import re  # Regular expression operations
import nltk  # Natural Language Toolkit for text processing
import spacy  # spaCy library for NLP tasks
from sklearn.metrics.pairwise import cosine_similarity  # For calculating similarity between vectors
from django.http import JsonResponse  # Used for sending JSON responses
from .models import Document  # Importing Document model
from django.views.decorators.csrf import csrf_exempt  # To exempt CSRF validation for this view
from sklearn.feature_extraction.text import TfidfVectorizer  # To transform text into TF-IDF vectors

# Download necessary resources for NLTK
nltk.download('stopwords')  # Stop words list used in text processing
nltk.download('punkt_tab')  # Tokenizer models for splitting text into words

@csrf_exempt
def semantic_search(request):
    """
    This view function takes a search query from the frontend, processes it, and finds the most
    semantically similar document in the Document model.
    """
    
    # Get the search query from the request
    query = request.GET.get('query', '')  # Retrieves the query parameter from the URL
    
    # Check if the query is empty
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    # If no query is provided, return a JSON response with an error message

    # Load spaCy's pre-trained NLP model for English
    nlp = spacy.load('en_core_web_md')
    
    # Fetch all documents from the database
    documents = Document.objects.all()

    # Debug: Print the document ids and contents
    for doc in documents:
        print(doc.id, doc.content)
    
    # Function to clean and preprocess text (lowercase and remove extra spaces)
    def preprocess_text(text):
        # Remove extra spaces and convert text to lowercase
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = text.lower()  # Convert text to lowercase for uniformity
        return text  # Return preprocessed text

    # Preprocess the content of all documents
    preprocessed_documents = [preprocess_text(doc.content) for doc in documents]
    print(f"Preprocessed text: {preprocessed_documents}")
    
    # Download the list of stopwords (common words like "and", "the", etc., that don’t add meaning to the text)
    stopwords = set(nltk.corpus.stopwords.words('english'))

    # Function to tokenize the text (split it into words) and remove stopwords
    def tokenize_and_remove_stopwords(text):
        # Use NLTK to tokenize the text (break it into individual words)
        tokens = nltk.word_tokenize(text)
        # Remove tokens that are not alphanumeric or are stopwords
        tokens = [token for token in tokens if token.isalnum() and token not in stopwords]
        return tokens  # Return the cleaned tokens

    # Tokenize and remove stopwords from all preprocessed documents
    tokenized_documents = [tokenize_and_remove_stopwords(doc) for doc in preprocessed_documents]
    # print(tokenized_documents)  # Uncomment this for debugging

    # Convert the tokenized documents into TF-IDF vectors (numerical representation of the text)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(tokens) for tokens in tokenized_documents])
    # print(tfidf_matrix)  # Debugging: You can print the TF-IDF matrix to check the results

    # Preprocess and tokenize the user query
    preprocessed_query = preprocess_text(query)  # Clean the user query
    tokenized_query = tokenize_and_remove_stopwords(preprocessed_query)  # Tokenize and remove stopwords from query
    
    # Convert the user query into a TF-IDF vector using the same vectorizer
    query_vector = vectorizer.transform([' '.join(tokenized_query)])  # Convert query to a vector

    # Calculate cosine similarity between the user query and all the documents
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    
    # Get the index of the document that is most similar to the user query
    most_similar_index = similarities[0].argmax()

    # Initialize a counter for looping through the documents
    count = 0
    for doc in documents:
        # Check if the current document matches the most similar index
        if count == most_similar_index:
            most_similar_document = doc.content  # Store the most similar document content
            break
        else:
            count += 1  # Increment the counter if the current document is not the most similar
    
    # Return the most similar document in the JSON response
    return JsonResponse({query: most_similar_document})
