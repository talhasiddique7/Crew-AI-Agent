# API Documentation

## CrewAI Service API

### Class: `CrewAIService`

Main service class for orchestrating CrewAI operations.

#### Constructor
```python
CrewAIService(config: AppConfig)
```

#### Methods

##### `summarize_youtube_video(url: str) -> Dict[str, Any]`
Summarize a YouTube video from its URL.

**Parameters:**
- `url` (str): YouTube video URL

**Returns:**
- Dictionary containing:
  - `success` (bool): Operation success status
  - `summary` (str): Generated summary
  - `transcript` (str): Original transcript
  - `video_id` (str): YouTube video ID
  - `transcript_length` (int): Transcript character count

**Example:**
```python
service = CrewAIService(config)
result = service.summarize_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
if result['success']:
    print(result['summary'])
```

##### `answer_academic_question(question: str) -> Dict[str, Any]`
Answer an academic question.

**Parameters:**
- `question` (str): Academic question to answer

**Returns:**
- Dictionary containing:
  - `success` (bool): Operation success status
  - `answer` (str): Generated answer
  - `question` (str): Original question
  - `answer_length` (int): Answer character count

**Example:**
```python
result = service.answer_academic_question("Explain photosynthesis")
if result['success']:
    print(result['answer'])
```

##### `test_connection() -> bool`
Test connection to Groq AI.

**Returns:**
- `bool`: True if connection successful

##### `get_service_status() -> Dict[str, Any]`
Get service status information.

**Returns:**
- Dictionary with service status details

## Utility Classes

### Class: `GroqLLMClient`

Professional Groq AI client for CrewAI integration.

#### Constructor
```python
GroqLLMClient(api_key: str, model: str = "llama3-8b-8192")
```

#### Methods

##### `generate(prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str`
Generate response using Groq AI.

### Class: `YouTubeTranscriptExtractor`

Handles YouTube transcript extraction.

#### Methods

##### `extract_video_id(url: str) -> Optional[str]`
Extract YouTube video ID from URL.

##### `extract_transcript_from_url(url: str) -> str`
Extract transcript directly from YouTube URL.

## Configuration

### Class: `AppConfig`

Application configuration settings.

#### Attributes
- `groq_api_key`: Groq API key
- `groq_model`: AI model name
- `app_title`: Application title
- `max_tokens_summary`: Maximum tokens for summaries
- `max_tokens_academic`: Maximum tokens for academic answers

## Error Handling

All methods include comprehensive error handling and return structured error information in case of failures.

### Common Exceptions
- `RuntimeError`: Service not properly initialized
- `Exception`: Various API and processing errors

### Error Response Format
```python
{
    'success': False,
    'error': 'Error message description',
    'result_key': None
}
```
